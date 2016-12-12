function velostat(Vi)
    Vo = 0;
    x = 0;
    R2 = 1;
    subplot(2,1,1)       % add first plot in 2 x 1 grid
    while R2 <= 10000
        for R1 = 200:10:2000;
            R = 200:10:2000;
            Req = R/(R1+R2);
            Vo = Vi.*Req;
        end
        plot(R, Vo ,'DisplayName', sprintf('R2 = %d', R2));
        if(x == 0)
            hold on;
            x = 1;
        end
        R2 = R2 * 10;
    end
    hold off;
    legend('show');
    xlabel('Rvelostat') % x-axis label
    ylabel('Vout') % y-axis label
    
    %--------------------------NEXT FUNCTION---------------------------%
    Vo = 0;
    x = 0;
    R2 = 1;
    subplot(2,1,2);       % add first plot in 2 x 1 grid
    while R2 <= 10000
        R1 = (200:10:2000);
        Req = R2./(R1+R2);
        Vo = Vi.*Req;
        plot((200:10:2000), Vo ,'DisplayName', sprintf('R2 = %d', R2));
        if(x == 0)
            hold on;
            x = 1;
        end
        R2 = R2 * 10;
    end
    hold off;
    legend('show');
    xlabel('Rvelostat') % x-axis label
    ylabel('Vout') % y-axis label
end