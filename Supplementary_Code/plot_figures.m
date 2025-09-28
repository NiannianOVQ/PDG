% Please replace the path below with the absolute path to your fractions.txt
load("C:\Users\YourName\Code_Supplementary\fraction.txt");

x = fraction(1,:);
y1 = fraction(2,:);
y2 = fraction(3,:);
y3 = fraction(4,:);
color1 = [0.843, 0.329, 0.145];
color2 = [0.008, 0.431, 0.761];
color3 = [0.494, 0.184, 0.549];
plot(x,y1,'Color', color1,'LineWidth', 2,'DisplayName','\it D')
hold on
plot(x,y2,'Color', color2,'LineWidth', 2,'DisplayName','\it C')
plot(x,y3,'Color', color3,'LineWidth', 2,'DisplayName','\it E')

ax = gca;
ax.FontSize = 17;

set(gca, 'XScale', 'log');
set(gca, 'XTick', [1, 10, 100, 1000, 10000]);
set(gca, 'XTickLabel', {'10^0', '10^1', '10^2', '10^3', '10^4'});
yticks([0, 0.2, 0.4, 0.6, 0.8, 1]);
yticklabels({'0', '0.2', '0.4', '0.6', '0.8', '1'});
ylim([-0.1, 1.1]);
xlabel('\it MCS', 'FontName', 'Times New Roman', 'FontSize', 20, 'FontWeight', 'bold');
ylabel('\it f', 'FontName', 'Times New Roman', 'FontSize', 20, 'FontWeight', 'bold');
legend('FontName', 'Times New Roman', 'Location','northeast','FontSize', 17,'Box', 'off')
