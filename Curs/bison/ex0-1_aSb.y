%{
#include <stdio.h>
%}

%%
input : start
        | start '\n' input
start :  
        | 'a' start 'b'
        ;

	 
%%
yylex() {
        int c;
        c = getchar();
        return c;
}

yyerror()
{
    printf("syntax error\n");
}

main()
{
    if(0==yyparse()) printf("Result yyparse OK\n");
}
