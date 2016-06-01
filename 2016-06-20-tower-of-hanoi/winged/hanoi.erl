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

% Some run-time configuration. set to either true or false
config(use_only_exact)         -> false; % false is faster
config(server_store_solutions) -> true.  % true is MUUUUCH faster (false uses naive approach with no caching/memoizing)

%% Commandline interface - use with erl -run ...
hanoi_cmdline(Args) ->
    [N|RestArgs] = Args,
    Solution = hanoi(list_to_integer(N)),

    case RestArgs of
        ["disable-output"] -> ok;
        []                 -> print_solution(Solution)
    end,
    erlang:halt().


%% Programming interface - you can specify only the first tower (2nd and 3rd are assumed empty)
hanoi(N) when is_integer(N) ->
    Server   = spawn_link(?MODULE, solution_server, [dict:new()]),
    Solution = calculate(N, Server),
    exit(Server, normal),
    Solution.


calculate(N, Server) when is_integer(N) ->
    calculate(N, a, b, c, Server).

calculate(1, From, To, _Via, _Server) ->
    [{action, move, From, To}];

calculate(N, From, To, Via, Server) ->
    Task = {task, N, From, To, Via},

    case get_solution(Task, Server) of
        no_solution ->
            Solution = calculate(N-1, From, Via, To, Server) ++ calculate(N-1, Via, To, From, Server),
            % Tell the server about our solution
            Server ! {solution, Task, Solution},

            [Task|Solution] ++ [end_of_task];
        {similar, Solution} -> [Task,{action, similar_solution,       Solution}] ++ [end_of_task];
        {exact,   Solution} -> [Task,{action, use_solution,     Task, Solution}] ++ [end_of_task]
    end.

indent(_, no_print) -> ok;
indent(0, Text)     -> io:format(Text);
indent(N, Text)     -> io:format(" "), indent(N-1, Text).

print_solution(Steps) -> print_solution(Steps, 0).

print_solution([], _)           -> ok;
print_solution([Step|Rest], Indent)  ->
    NewIndent = case Step of
        end_of_task -> Indent - 1;
        {task, _N, _F, _T, _V}   -> Indent + 1;
        _Other      -> Indent
    end,
    indent(Indent, step_display(Step)),
    print_solution(Rest, NewIndent),
    ok.

step_display(end_of_task) -> no_print;
step_display({task, N, From, To, Via})         -> io_lib:format("Task: Move ~w pieces from ~w to ~w via ~w~n", [N, From, To, Via]);
step_display({action,move,         From, To})  -> io_lib:format("Action: Move single piece from ~w to ~w~n", [From, To]);
step_display({action,use_solution, {task, N, From, To, Via}, _Steps})  ->
    io_lib:format(
        "Repeat steps from last time when you moved ~w pieces from ~w to ~w via ~w~n",
     [
      N, From, To, Via % old task description
     ]);
step_display({action,similar_solution, {{{task, N, From, To, Via}, {task, N, F2, T2, V2}}, _Steps}})  ->
    io_lib:format(
        "Repeat steps from last time when you moved ~w pieces from ~w to ~w via ~w, but replace as follows: ~w -> ~w, ~w -> ~w, ~w -> ~w~n",
     [
      N, F2, T2, V2, % old task description,

      F2, From, % from replacement
      T2, To,   % to replacement
      V2, Via   % via replacement
     ]);
step_display(Step) ->
    io_lib:format("Ugh... unhandled step description: ~w~n", [Step]).


get_solution(Task, Server) ->
    Server ! {self(), Task},
    receive Result -> Result
    after 1000     -> {error, server_dead}
    end.

solution_server(Solutions) ->
    receive {Client, {task, _N, _From, _To, _Via}=Task} ->
                Solution = server_select_solution(Task, Solutions),
                Client ! Solution,
                solution_server(Solutions);
            {solution, {task, _N, _From, _To, _Via}=Task, _Solution} ->
                case config(server_store_solutions) of
                    true  -> solution_server(dict:store(Task, lookitupyourself, Solutions));
                    false -> solution_server(Solutions)
                end;
            Unknown ->
                io:format("Solution server: unknown message ~w~n~n", [Unknown]),
                solution_server(Solutions)
    end.


server_select_solution({task, N, A, B, C}=Task, Solutions) ->
    Variants = [
                {task, N, A, B, C}, % same as Task
                {task, N, A, C, B},
                {task, N, B, A, C},
                {task, N, B, C, A},
                {task, N, C, B, A},
                {task, N, C, A, B}
               ],

    Solution = server_select_solution(Task, Variants, Solutions),

    case Solution of
        no_solution -> no_solution;
        {ok, Variant, Steps} ->
            case Variant of
                Task   -> {exact,   Steps};
                _Other -> case config(use_only_exact) of
                              true  -> no_solution;
                              false -> {similar, {{Task, Variant}, Steps}}
                          end
            end
    end.

server_select_solution(_Task, [],            _Solutions) -> no_solution;
server_select_solution(Task,  [Variant|Rest], Solutions) ->
    case dict:is_key(Variant, Solutions) of
        true   -> {ok, Variant, dict:fetch(Variant, Solutions)};
        false  -> server_select_solution(Task, Rest, Solutions)
    end.

% vim: set sw=4 ts=4 et:
