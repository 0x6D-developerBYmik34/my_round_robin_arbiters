module simple_arbiter #(
    parameter REQUASTERS_QUANT = 2
) (
    input clk,
    input rst,
    input logic [REQUASTERS_QUANT - 1:0] req,
    output logic [REQUASTERS_QUANT - 1:0] grants 
);

    logic [REQUASTERS_QUANT - 1:0] static_req, static_grants, pointer_req;
    logic [$clog2(REQUASTERS_QUANT) - 1:0] ptr, new_ptr;

    // cycle shifts with ptr for static arbiter 
    assign static_req = (req >> ptr) | (req << (REQUASTERS_QUANT - ptr));
    assign grants = (static_grants << ptr) | (static_grants  >> (REQUASTERS_QUANT - ptr));

    // static arbiter
    always_comb begin
        static_grants = 'b0;
        for (int i = REQUASTERS_QUANT - 1; i >= 0; i--)
            if (static_req[i]) begin
                static_grants = (1'b1 << i);
            end
    end
    // .....
   
    // pointer logic
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
        if (rst) ptr <= 'b0;
        else ptr <= ptr + new_ptr;
    // ....

endmodule
