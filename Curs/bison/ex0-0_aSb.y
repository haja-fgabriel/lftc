%{
#include <stdio.h>
%}

%%
S :     'a' S 'b'
     |  'a'  'b'
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
    if(0==yyparse()) printf("Result yyparse: OK\n");
}
