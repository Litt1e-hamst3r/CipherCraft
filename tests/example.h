// example.h

#ifdef EXAMPLE_EXPORTS
#define EXAMPLE_API __declspec(dllexport)
#else
#define EXAMPLE_API __declspec(dllimport)
#endif

extern "C" {
    EXAMPLE_API int add(int a, int b);
}