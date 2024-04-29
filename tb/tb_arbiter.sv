module testbench;

    // Тактовый сигнал и сигнал сброса
    logic clk;
    logic rst;

    // Остальные сигналы (combs)
    logic [7:0] req, grants;

    simple_arbiter #(8) dut(.clk(clk), .rst(rst), .req(req), .grants(grants));

    // Период тактового сигнала
    parameter CLK_PERIOD = 10;

    // Генерация тактового сигнала
    initial begin
        clk <= 0;
        forever begin
            #(CLK_PERIOD/2) clk <= ~clk;
        end
    end

    // Генерация сигнала сброса
    task reset();
        rst <= 1;
        #(CLK_PERIOD);
        rst <= 0;
    endtask

    // мониторим
    task monchi();
        wait(!rst);
        forever begin
            @(posedge clk);
            $monitor("req=%b, grants=%b", req, grants);
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
        wait(!rst);
        @(posedge clk);
        req = 8'b10011011;
        @(posedge clk);
        req = 8'b10011010;
        @(posedge clk);
        req = 8'b10011000;
        @(posedge clk);
        req = 8'b10011000;
        @(posedge clk);
        req = 8'b10001010;
        @(posedge clk);
        req = 8'b00001010;
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
        wait(!rst);
        @(posedge clk);
        req = 8'b10011010;
        @(posedge clk);
        req = 8'b10011000;
        @(posedge clk);
        req = 8'b10011000;
        @(posedge clk);
        req = 8'b10001010;
        @(posedge clk);
        req = 8'b00001010;
        @(posedge clk);
        disable fork;
    endtask

    task test_case_3();
        $display("TESTCASE 3");
        fork
            reset();
            monchi();
        join_none
        req = 8'b0;
        wait(!rst);
        @(posedge clk);
        req = 8'b11111111;
        repeat(8) begin
            @(posedge clk);
        end
        disable fork;
    endtask

    initial begin
        test_case_1();      
        test_case_2();      
        test_case_3();      
        $finish();
    end
    // ......

 endmodule
