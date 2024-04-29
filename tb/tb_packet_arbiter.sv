`timescale 1ns/10ps

module testbench;

    // Тактовый сигнал и сигнал сброса
    logic clk;
    logic rst;

    // Остальные сигналы (combs)
    logic [7:0] req, grants, req_is_last;

    simple_rr_packet_arbiter #(8) dut (
        .clk(clk), .rst(rst), .req(req), .req_is_last(req_is_last), .grants(grants)
    );

    // Период тактового сигнала
    parameter CLK_PERIOD = 10;

    // Генерация тактового сигнала
    initial begin
        clk <= 0;
        forever begin
            #(CLK_PERIOD / 2) clk <= ~clk;
        end
    end

    // Генерация сигнала сброса
    task reset();
        rst <= 1;
        #(CLK_PERIOD);
        #(CLK_PERIOD / 2);
        rst <= 0;
    endtask

    // мониторим
    task monchi();
        wait(!rst);
        forever begin
            @(posedge clk);
            $monitor(
                "req=%b, req_is_last=%b, grants=%b", 
                req, req_is_last, grants
            );
        end
    endtask

    // Генерация входных сигналов
    task test_case_1();
        $display("TESTCASE 1");
        fork
            reset();
            monchi();
        join_none
        req = 8'b0;
        req_is_last = 8'bx;
        wait(!rst);
        @(posedge clk);
        req =         8'b10011011;
        req_is_last = 8'b00000000;
        @(posedge clk);
        req =         8'b10011011;
        req_is_last = 8'b00000001;
        @(posedge clk);
        req =         8'b10011010;
        req_is_last = 8'b00000000;
        @(posedge clk);
        req =         8'b10011011;
        req_is_last = 8'b00000010;
        @(posedge clk);
        req =         8'b10011001;
        req_is_last = 8'b00000000;
        @(posedge clk);
        req =         8'b10011001;
        req_is_last = 8'b00001000;
        @(posedge clk);
        req =         8'b10010001;
        req_is_last = 8'b00000000;
        @(posedge clk);
        req =         8'b10110001;
        req_is_last = 8'b00010000;
        @(posedge clk);
        req =         8'b10100001;
        req_is_last = 8'b00000000;
        @(posedge clk);
        req =         8'b10100001;
        req_is_last = 8'b00000000;
        @(posedge clk);
        req =         8'b10100001;
        req_is_last = 8'b00000000;
        @(posedge clk);
        disable fork;
    endtask

    task test_case_2();
        $display("TESTCASE 2");
        fork
            reset();
            monchi();
        join_none
        req = 8'b0;
        req_is_last = 8'b0;
        wait(!rst);
        @(posedge clk);
        req = 8'b11111111;
        req_is_last = 8'b11111111;
        repeat(7) begin
            @(posedge clk);
        end
        disable fork;
    endtask

    initial begin
        $dumpfile("out/tb.vcd");
        $dumpvars(2, testbench);
        test_case_1();      
        test_case_2();
        $finish();
    end
    // ......

 endmodule
