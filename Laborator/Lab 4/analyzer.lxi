%{
#include <iostream>
#include <vector>
#include <map>
#include <string>

using namespace std;

vector<int> elems;
map<string, int> symbols;

struct Token {
    int type;
    int identifierCount;
    string what;
    bool isIdOrConst() {
        return type < 4;
    }
};

map<string, int> atoms = {
    {"id",          1},
    {"int_const",   2},
    {"float_const", 3},
    {"while",       4},
    {"{",           5},
    {"}",           6},
    {"int",         7},
    {"float",       8},
    {"char",        9},
    {",",           10},
    {"return",      11},
    {"print",       12},
    {"scan",        13},
    {"(",           14},
    {")",           15},
    {";",           16},
    {"=",           17},
    {"+",           18},
    {"-",           19},
    {"%",           20},
    {"/",           21},
    {"repeat",      22},
    {"until",       23},
    {"<",           24},
    {">",           25},
    {"<=",          26},
    {">=",          27}
};

vector<Token> internalRepr;


int numSymbols;
int line;
int column;

%}

%option noyywrap

DIGIT [0-9]
NON-NULL-DIGIT [1-9]
INT-CONST ("-")?([1-9][0-9]*|0)
FLOAT-CONST ("-")?((([1-9][0-9]*|0)[.][0-9]*)|(([1-9][0-9]*|0)?[.][0-9]+))
CURLY-BRACE "{"|"}"
ID [_$a-zA-Z][_$a-zA-Z0-9]{0,7}
OPT-KEYWORD return|exit
KEYWORD while|continue|break|if|scan|print|repeat|until
PARANTHESES "("|")"
SIGN "="|"+"|"-"|"*"|"/"|"%"|(("<"|">")"="?)
TYPE int|char|float
SEPARATOR ","|";"

%%


{CURLY-BRACE}|{KEYWORD}|{OPT-KEYWORD}|{PARANTHESES}|{SIGN}|{TYPE}|{SEPARATOR} {
    //cout << "Found  something else:  " << yytext << endl;
    internalRepr.push_back({atoms[yytext], -1, yytext});
    column += yyleng;
}


{FLOAT-CONST} {
    if (symbols.find(yytext) == symbols.end()) {
        ++numSymbols;
        symbols[yytext] = numSymbols; 
    }
    internalRepr.push_back({3, symbols[yytext], yytext});
    column += yyleng;
}

{INT-CONST} {
    if (symbols.find(yytext) == symbols.end()) {
        ++numSymbols;
        symbols[yytext] = numSymbols; 
    }
    internalRepr.push_back({2, symbols[yytext], yytext});
    column += yyleng;
}

{ID} {
    if (symbols.find(yytext) == symbols.end()) {
        ++numSymbols;
        symbols[yytext] = numSymbols; 
    }
    internalRepr.push_back({1, symbols[yytext], yytext});
    column += yyleng;
}

"\n" {
    line++; column = 1;
}

" "|"\t" {
    column++;
}

"//"[^\n]* {
    //cout << "Found one-line comment\n";
    line++;
    column = 1;
}

. {
    cerr << "Error while analyzing file at line " << line << ", column " << column << '\n';
    return 1;
}

%%


void printSymbolTable() {
    cout << "Code of symbol\tSymbol:\n";
    for (auto sym : symbols) {
        cout << sym.second << "\t\t" << sym.first << endl;
    }
}

void printInternalRepresentation() {
    cout << "Atom value\tSym table value" << endl;
    for (auto tok : internalRepr) {
        cout << tok.type << "\t\t"; 
        if (tok.isIdOrConst())
            cout << tok.identifierCount << ' ';
        else
            cout << "- ";//\n";
        cout << endl;
    }
}

int main(int argc, char** argv) {
    if (argc < 2)  {
        cerr << "Usage: " << argv[0] << " <input_file>\n";
        return 1;
    }
    else {
        yyin = fopen( argv[1], "r" );
    }
    line = 1;   
    column = 1;
    if (!yylex()) {
        printSymbolTable();
        cout << endl;
        printInternalRepresentation();
    }

    return 0;
}


/*

NOTE: Please leave the useless expressions there, since you cannot
comment in the rules section

------------ GARBAGE ----------------


"//"[^\n]* 

-------------------------------------

*/