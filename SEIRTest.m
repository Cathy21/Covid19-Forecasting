A = 28112;
beta = .5;
c = .12;
d = .0058;
delta = .0685;
alpha = .6;%1/5.2;
eta = 1/14;
rho1 = .64;
rho2 = .78;
b1 = .07122;
b2 = .11013;
sigma = 0;%.119732;
p = .96657;
%M = .916499;
M=0;

rhs = @(t, xt) [A - beta*(1-rho1)*(1-rho2)*xt(1)*xt(2) + b1*xt(3) - d*xt(1) - p*xt(1)*M;
    beta*(1-rho1)*(1-rho2)*xt(1)*xt(2) - b2*xt(2) - alpha*xt(2) - sigma*xt(2) - d*xt(2);
    b2*xt(2) - b1*xt(3) - c*xt(3) - d*xt(3);
    alpha*xt(2) + c*xt(3) - (eta + d + delta)*xt(4);
    eta*xt(4) + sigma*xt(2) - d*xt(5) + p*xt(1)*M];

x0 = [1374333, 312, 945, 0, 0];
[time, x] = ode45(rhs,[0,50],x0);

figure(1)
plot(time, x);
xlabel('Time');
ylabel('Number of Individuals');
legend('S','E','Q','I','R');