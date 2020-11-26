%{
#include <stdio.h>
%}

%token NUMBER

%%
line : expr '\n'         { printf("line OK\n");}
    
expr : expr expr '+'
		| expr expr '*'
		| NUMBER
     ;


%%

yyerror() {
    printf("syntax error\n");
}
        
        

main() {
    yyparse();
}

    