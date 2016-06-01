%%% Run using the following commands
%%% (the 5 is the height of the initial stack):
%%%
%%% erlc hanoi.erl && erl -noshell -exit -run hanoi hanoi_cmdline 5

-module(hanoi).

-export([
         hanoi/1,
         hanoi_cmdline/1,
         solution_server/1
        ]).

%% Commandline interface - use with erl -run ...
hanoi_cmdline(Args) ->
    [N|_] = Args,
    Solution = hanoi(list_to_integer(N)),
    print_solution(Solution),
    erlang:halt().


%% Programming interface - you can specify only the first tower (2nd and 3rd are assumed empty)
hanoi(N) when is_integer(N) ->
    Server   = spawn_link(?MODULE, solution_server, [dict:new()]),
    %io:format("Server: ~w~n", [Server]),
    Solution = calculate(N, Server),
    exit(Server, normal),
    Solution.


calculate(N, Server) when is_integer(N) ->
    calculate(N, a, b, c, Server).

calculate(1, From, To, _Via, _Server) ->
    [{{action, move, From, To}}];

calculate(N, From, To, Via, Server) ->
    Task = {task, From, To, Via},

    case get_solution(Task, Server) of
        no_solution ->
            Solution = [
                        Task |
                        calculate(N-1, From, Via, To, Server) ++ 
                        calculate(N-1, Via, To, From, Server)
                       ],
            % Tell the server about our solution
            Server ! {solution, Task, Solution},

            Solution;
        Solution -> 
            Action = {action, use_existing_solution, Solution},

            [Task, Action]
    end.

print_solution([])           -> ok;
print_solution([Step|Rest])  ->
    % note the reversed order - we prepend new steps when calculating, so we
    % have to print the "current" step after all others
    io:format("~w~n", [Step]),
    print_solution(Rest),
    ok.

get_solution(Task, Server) ->
    Server ! {self(), Task},
    receive Result -> Result
    after 10       -> {error, server_dead}
    end.

solution_server(Solutions) ->
    receive {From, {task, _From, _To, _Via}=Task} ->
                case dict:is_key(Task, Solutions) of
                    true   -> From ! dict:fetch(Task, Solutions);
                    false  -> From ! no_solution
                end,
                solution_server(Solutions);
            {solution, {task, _From, _To, _Via}=Task, Solution} ->
                solution_server(dict:store(Task, Solution, Solutions));
            Unknown ->
                io:format("Solution server: unknown message ~w~n~n", [Unknown]),
                solution_server(Solutions)
    end.


% vim: set sw=4 ts=4 et:
