module EEE_IMGPROC(
	// global clock & reset
	clk,
	reset_n,
	
	// mm slave
	s_chipselect,
	s_read,
	s_write,
	s_readdata,
	s_writedata,
	s_address,

	// stream sink
	sink_data,
	sink_valid,
	sink_ready,
	sink_sop,
	sink_eop,
	
	// streaming source
	source_data,
	source_valid,
	source_ready,
	source_sop,
	source_eop,
	
	// conduit
	mode
	
);


// global clock & reset
input	clk;
input	reset_n;

// mm slave
input							s_chipselect;
input							s_read;
input							s_write;
output	reg	[31:0]	s_readdata;
input	[31:0]				s_writedata;
input	[2:0]					s_address;


// streaming sink
input	[23:0]            	sink_data;
input								sink_valid;
output							sink_ready;
input								sink_sop;
input								sink_eop;

// streaming source
output	[23:0]			  	   source_data;
output								source_valid;
input									source_ready;
output								source_sop;
output								source_eop;

// conduit export
input                         mode;

////////////////////////////////////////////////////////////////////////
//
parameter IMAGE_W = 11'd640;
parameter IMAGE_H = 11'd480;
parameter MESSAGE_BUF_MAX = 256;
parameter MSG_INTERVAL = 12;
parameter BB_COL_DEFAULT = 24'h00ff00;


wire [7:0]   red, green, blue, grey;
wire [7:0]   red_out, green_out, blue_out;

wire         sop, eop, in_valid, out_ready;
////////////////////////////////////////////////////////////////////////

// Detect coloured areas

// Detect white for maze walls
wire white_detect;
assign white_detect = (red[7] & green[7] & blue[7]) && (x > (IMAGE_W/2)) && (x < IMAGE_W) &&(y >= (IMAGE_H/2)) && (y < IMAGE_H);

// Detect other colours for beacons	 
wire red_detect;
assign red_detect = (red[7] & ~green[7] & ~blue[7] ) && (x >= IMAGE_W/3) && (x < (2*IMAGE_W/3));

wire blue_detect;
assign blue_detect = (~red[7] & ~green[7] & blue[7]) && (x >= IMAGE_W/3) && (x < (2*IMAGE_W/3));

wire yellow_detect;
assign yellow_detect = (red[7] & green[7] & ~blue[7]) && (x >= IMAGE_W/3) && (x < (2*IMAGE_W/3));

assign grey = green[7:1] + red[7:2] + blue[7:2]; //Grey = green/2 + red/4 + blue/4

// Show bounding boxes and highlight detected areas
wire [23:0] new_image;
wire bb_active_w;
wire bb_active_r;
wire bb_active_b;
wire bb_active_y;
assign bb_active_w = (x == left_w) | (x == right_w) | (y == top_w) | (y == bottom_w);
assign bb_active_r = (x == left_r) | (x == right_r) | (y == top_r) | (y == bottom_r);
assign bb_active_b = (x == left_b) | (x == right_b) | (y == top_b) | (y == bottom_b); 
assign bb_active_y = (x == left_y) | (x == right_y) | (y == top_y) | (y == bottom_y);
assign new_image = bb_active_w | bb_active_r | bb_active_b | bb_active_y ? bb_col : white_detect ? {8'hff, 8'hff, 8'hff} : red_detect ? {8'hff, 8'h00, 8'h00} : blue_detect ? {8'h00, 8'h00, 8'hff} : yellow_detect ? {8'hff, 8'hff, 8'h00} : {grey, grey, grey};

// Switch output pixels depending on mode switch
// Don't modify the start-of-packet word - it's a packet discriptor
// Don't modify data in non-video packets
assign {red_out, green_out, blue_out} = (mode & ~sop & packet_video) ? new_image : {red,green,blue};

//Count valid pixels to get the image coordinates. Reset and detect packet type on Start of Packet.
reg [10:0] x, y;
reg packet_video;
always@(posedge clk) begin
	if (sop) begin
		x <= 11'h0;
		y <= 11'h0;
		packet_video <= (blue[3:0] == 3'h0);
	end
	else if (in_valid) begin
		if (x == IMAGE_W-1) begin
			x <= 11'h0;
			y <= y + 11'h1;
		end
		else begin
			x <= x + 11'h1;
		end
	end
end

//Find first and last of each of the coloured pixels
reg [10:0] x_min_w, y_min_w, x_max_w, y_max_w;
reg [10:0] x_min_r, y_min_r, x_max_r, y_max_r;
reg [10:0] x_min_b, y_min_b, x_max_b, y_max_b;
reg [10:0] x_min_y, y_min_y, x_max_y, y_max_y;
always@(posedge clk) begin
	if (white_detect && in_valid) begin	//Update bounds when the pixel is white
		if (x < x_min_w) x_min_w <= x;
		if (x > x_max_w) x_max_w <= x;
		if (y < y_min_w) y_min_w <= y;
		y_max_w <= y;
	end
	if (red_detect && in_valid) begin	//Update bounds when the pixel is red
		if (x < x_min_r) x_min_r <= x;
		if (x > x_max_r) x_max_r <= x;
		if (y < y_min_r) y_min_r <= y;
		y_max_r <= y;
	end
	if (blue_detect && in_valid) begin	//Update bounds when the pixel is blue
		if (x < x_min_b) x_min_b <= x;
		if (x > x_max_b) x_max_b <= x;
		if (y < y_min_b) y_min_b <= y;
		y_max_b <= y;
	end
	if (yellow_detect && in_valid) begin	//Update bounds when the pixel is yellow
		if (x < x_min_y) x_min_y <= x;
		if (x > x_max_y) x_max_y <= x;
		if (y < y_min_y) y_min_y <= y;
		y_max_y <= y;
	end
	if (sop && in_valid) begin	//Reset bounds on start of packet
		x_min_w <= IMAGE_W-11'h1;
		x_max_w <= 0;
		y_min_w <= IMAGE_H-11'h1;
		y_max_w <= 0;
		x_min_r <= IMAGE_W-11'h1;
		x_max_r <= 0;
		y_min_r <= IMAGE_H-11'h1;
		y_max_r <= 0;
		x_min_b <= IMAGE_W-11'h1;
		x_max_b <= 0;
		y_min_b <= IMAGE_H-11'h1;
		y_max_b <= 0;
		x_min_y <= IMAGE_W-11'h1;
		x_max_y <= 0;
		y_min_y <= IMAGE_H-11'h1;
		y_max_y <= 0;
	end
end

//Process bounding box at the end of the frame.
reg [2:0] msg_state;
reg [10:0] left_w, right_w, top_w, bottom_w;
reg [10:0] left_r, right_r, top_r, bottom_r;
reg [10:0] left_b, right_b, top_b, bottom_b;
reg [10:0] left_y, right_y, top_y, bottom_y;
reg [7:0] frame_count;
always@(posedge clk) begin
	if (eop & in_valid & packet_video) begin  //Ignore non-video packets
		
		//Latch edges for display overlay on next frame
		left_w <= x_min_w;
		right_w <= x_max_w;
		top_w <= y_min_w;
		bottom_w <= y_max_w;

		left_r <= x_min_r;
		right_r <= x_max_r;
		top_r <= y_min_r;
		bottom_r <= y_max_r;

		left_b <= x_min_b;
		right_b <= x_max_b;
		top_b <= y_min_b;
		bottom_b <= y_max_b;

		left_y <= x_min_y;
		right_y <= x_max_y;
		top_y <= y_min_y;
		bottom_y <= y_max_y;

		
		
		//Start message writer FSM once every MSG_INTERVAL frames, if there is room in the FIFO
		frame_count <= frame_count - 1;
		
		if (frame_count == 0 && msg_buf_size < MESSAGE_BUF_MAX - 3) begin
			msg_state <= 3'b000;
			frame_count <= MSG_INTERVAL-1;
		end
	end
	
	//Cycle through message writer states once started
	msg_state <= msg_state + 3'b001;

end
	
//Generate output messages for CPU
reg [31:0] msg_buf_in; 
wire [31:0] msg_buf_out;
reg msg_buf_wr;
wire msg_buf_rd, msg_buf_flush;
wire [7:0] msg_buf_size;
wire msg_buf_empty;


always@(*) begin	//Write words to FIFO as state machine advances
	case(msg_state)
		3'b000: begin
			msg_buf_in = {5'b00000, x_min_w, 5'b0, x_max_w}; //white width
			msg_buf_wr = 1'b1;
		end
		3'b001: begin
			msg_buf_in = {5'b00001, y_min_w, 5'b0, y_max_w};	//white height
			msg_buf_wr = 1'b1;
		end
		3'b010: begin
			msg_buf_in = {5'b00010, x_min_r, 5'b0, x_max_r};	//red width
			msg_buf_wr = 1'b1;
		end
		3'b011: begin
			msg_buf_in = {5'b00011, y_min_r, 5'b0, y_max_r};	//red height
			msg_buf_wr = 1'b1;
		end
		3'b100: begin
			msg_buf_in = {5'b00100, x_min_b, 5'b0, x_max_b};	//blue width
			msg_buf_wr = 1'b1;
		end
		3'b101: begin
			msg_buf_in = {5'b00101, y_min_b, 5'b0, y_max_b};	//blue height
			msg_buf_wr = 1'b1;
		end
		3'b110: begin
			msg_buf_in = {5'b00110, x_min_y, 5'b0, x_max_y};		//yellow width
			msg_buf_wr = 1'b1;
		end
		3'b011: begin
			msg_buf_in = {5'b00111, y_min_y, 5'b0, y_max_y};	//yellow height
			msg_buf_wr = 1'b1;
		end
	endcase
end


//Output message FIFO
MSG_FIFO	MSG_FIFO_inst (
	.clock (clk),
	.data (msg_buf_in),
	.rdreq (msg_buf_rd),
	.sclr (~reset_n | msg_buf_flush),
	.wrreq (msg_buf_wr),
	.q (msg_buf_out),
	.usedw (msg_buf_size),
	.empty (msg_buf_empty)
	);


//Streaming registers to buffer video signal
STREAM_REG #(.DATA_WIDTH(26)) in_reg (
	.clk(clk),
	.rst_n(reset_n),
	.ready_out(sink_ready),
	.valid_out(in_valid),
	.data_out({red,green,blue,sop,eop}),
	.ready_in(out_ready),
	.valid_in(sink_valid),
	.data_in({sink_data,sink_sop,sink_eop})
);

STREAM_REG #(.DATA_WIDTH(26)) out_reg (
	.clk(clk),
	.rst_n(reset_n),
	.ready_out(out_ready),
	.valid_out(source_valid),
	.data_out({source_data,source_sop,source_eop}),
	.ready_in(source_ready),
	.valid_in(in_valid),
	.data_in({red_out, green_out, blue_out, sop, eop})
);


/////////////////////////////////
/// Memory-mapped port		 /////
/////////////////////////////////

// Addresses
`define REG_STATUS    			0
`define READ_MSG    				1
`define READ_ID    				2
`define REG_BBCOL					3

//Status register bits
// 31:16 - unimplemented
// 15:8 - number of words in message buffer (read only)
// 7:5 - unused
// 4 - flush message buffer (write only - read as 0)
// 3:0 - unused


// Process write

reg  [7:0]   reg_status;
reg	[23:0]	bb_col;

always @ (posedge clk)
begin
	if (~reset_n)
	begin
		reg_status <= 8'b0;
		bb_col <= BB_COL_DEFAULT;
	end
	else begin
		if(s_chipselect & s_write) begin
		   if      (s_address == `REG_STATUS)	reg_status <= s_writedata[7:0];
		   if      (s_address == `REG_BBCOL)	bb_col <= s_writedata[23:0];
		end
	end
end


//Flush the message buffer if 1 is written to status register bit 4
assign msg_buf_flush = (s_chipselect & s_write & (s_address == `REG_STATUS) & s_writedata[4]);


// Process reads
reg read_d; //Store the read signal for correct updating of the message buffer

// Copy the requested word to the output port when there is a read.
always @ (posedge clk)
begin
   if (~reset_n) begin
	   s_readdata <= {32'b0};
		read_d <= 1'b0;
	end
	
	else if (s_chipselect & s_read) begin
		if   (s_address == `REG_STATUS) s_readdata <= {16'b0,msg_buf_size,reg_status};
		if   (s_address == `READ_MSG) s_readdata <= {msg_buf_out};
		if   (s_address == `READ_ID) s_readdata <= 32'h1234EEE2;
		if   (s_address == `REG_BBCOL) s_readdata <= {8'h0, bb_col};
	end
	
	read_d <= s_read;
end

//Fetch next word from message buffer after read from READ_MSG
assign msg_buf_rd = s_chipselect & s_read & ~read_d & ~msg_buf_empty & (s_address == `READ_MSG);
						


endmodule

