module simple_rr_packet_arbiter #(
    parameter REQUASTERS_QUANT = 2
) (
    input clk,
    input rst,
    input logic [REQUASTERS_QUANT - 1:0] req,
    input logic [REQUASTERS_QUANT - 1:0] req_is_last,
    output logic [REQUASTERS_QUANT - 1:0] grants 
);

    // make is a typedef
    logic [REQUASTERS_QUANT - 1:0] static_req, 
        static_grants, pointer_req;
    logic [$clog2(REQUASTERS_QUANT) - 1:0] ptr, new_ptr, calc_ptr;

    // cycle shifts with ptr for static arbiter 
    assign static_req = (req >> ptr) | (req << (REQUASTERS_QUANT - ptr));
    assign grants = (static_grants << ptr) | (static_grants  >> (REQUASTERS_QUANT - ptr));
    
    wire grant_is_last = |(req_is_last & grants);

    // static arbiter
    always_comb begin
        static_grants = 'b0;
        for (int i = REQUASTERS_QUANT - 1; i >= 0; i--)
            if (static_req[i]) begin
                static_grants = (1'b1 << i);
            end
    end
    // .....
   
    // pointer calc logic
    assign pointer_req = static_req ^ static_grants;
    
    always_comb begin
        new_ptr = 'b0;
        for (int i = REQUASTERS_QUANT - 1; i >= 0; i--)
            if (pointer_req[i]) begin
                new_ptr = i;
            end
    end
    // ....
    
    // pointer update
    always_ff @(posedge clk or posedge rst)
        if (rst) calc_ptr <= 'b0;
        else if(update_calc_ptr) calc_ptr <= new_ptr;

    always_ff @(posedge clk or posedge rst)
        if (rst) ptr <= 'b0;
        else if(grant_is_last) 
            ptr <= ptr + (force_update_ptr ? new_ptr : calc_ptr);
    // ....
    
    // FSM update pointer logic
    enum bit [1:0] {
        IDLE,
        RECIV_PACKET,
        LAST_IN_PACKET
    } prev_state, curr_state;

    always_comb
        if (grant_is_last) curr_state = LAST_IN_PACKET;
        else if (~(|req))  curr_state = IDLE;
        else curr_state = RECIV_PACKET;

    wire update_calc_ptr = 
        (prev_state != RECIV_PACKET) && (curr_state == RECIV_PACKET);
    wire force_update_ptr = 
        (prev_state != RECIV_PACKET) && (curr_state == LAST_IN_PACKET);

    always_ff @(posedge clk or posedge rst)
        if (rst) prev_state <= IDLE;
        else prev_state <= curr_state;
    // ....

endmodule
