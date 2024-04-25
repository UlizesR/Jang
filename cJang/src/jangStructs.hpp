// jangStructs.hpp
#ifndef JANGSTRUCTS_H
#define JANGSTRUCTS_H

#include <string>
#include <any>
#include <vector>

typedef struct jangVar
{
    std::string name;
    std::string type;
    std::any value;
} jangVar;

typedef struct jangFunc
{
    std::string name;
    std::string returnType;
    std::vector<jangVar> args;
    std::string body;
    bool isMethod;
} jangFunc;

typedef struct jangClass
{
    std::string name;
    std::vector<jangVar> vars;
    std::vector<jangFunc> funcs;
} jangClass;

typedef struct jangWhileLoop
{
    std::string condition;
    std::string body;
} jangWhileLoop;

typedef struct jangForLoop
{
    std::string init;
    std::string condition;
    std::string update;
    std::string body;
} jangForLoop;

typedef struct jangIf
{
    std::string condition;
    std::string body;
    std::string elseBody;
} jangIf;

#endif // JANGSTRUCTS_H