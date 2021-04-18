close all;
clear all;
load Xraw  %Currently using data from India SEIR paper

I0 = 15; %hardcoded for now
N = 1374333; %hardcoded for now
[theta, fmin] = fminsearch(@(theta) paramError(theta, Xraw, N, I0), [.25,1/7]); %guess beta = .25, gamma = 1/7

beta = theta(1);
gamma = theta(2);

rhs = @(t, xt) [-beta*xt(1)*xt(2)/N;
    beta*xt(1)*xt(2)/N - gamma*xt(2);
    gamma*xt(2)];

x0 = [N, I0, 0];
[time, xsol] = ode45(rhs,[0,60],x0);
figure(1)
plot(time, xsol(:,2));
hold on
plot(time, xsol(:,3));
plot(x, Xraw(:,2))
plot(x, Xraw(:,3))
xlabel('Time');
ylabel('Number of Individuals');
legend('I (model)','R (model)','I (data)','R (data)');

%find the Sum Squared Error of the I and R curves for the model with params
%theta
function obj = paramError(theta, X, N, I0)
    beta = theta(1);
    gamma = theta(2);
    rhs = @(t, xt) [-beta*xt(1)*xt(2)/N;
        beta*xt(1)*xt(2)/N - gamma*xt(2);
        gamma*xt(2)];

    x0 = [1374333, I0, 0];
    [time, xsol] = ode45(rhs,[0,50],x0);
    
    [s,~] = size(X);
    yint = 1:s;
    
    modelInf = spline(time, xsol(:,2), yint);
    modelRec = spline(time, xsol(:,3), yint);
    
    obj = 0;
    for i = 1:s % Calculate the SSE's for the model
        obj = obj + (modelInf(i) - X(i,2))^2;
        obj = obj + (modelRec(i) - X(i,3))^2;
    end
end