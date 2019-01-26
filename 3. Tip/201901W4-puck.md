## 写在前面
这周把设计模式的课程撸完了。感受就是在C++中，有些时候面向对象提供的基于虚函数的多态效率损失是不能忍受的。比如常用的iterator模式，常用与循环，每一步都虚函数动态绑定实在是又没必要又蛋疼的一件事情。《设计模式》这本书是94年左右写的，在98年左右，当STL出世时，大家发现STL以模板实现的迭代器这么好用的时候，就再也没人写面向对象的迭代器了。在这些情况下，模板某种程度上实现了一种编译时多态的技术。

以上，促成了我深入学习模板最大的动力。毕竟，有哪个程序员不希望写复用性最强的类框架代码呢？
## 模版元编程（00）
p.s.：程序员特色，我要从0开始编号了！

- 最基本的元函数，返回类型本身
    ```c++
    template <typename T>
    struct TypeIdentity
    {
        using type = T;
    };
    ```
- 返回传入类型的指针类型
    ```c++
    template <typename T>
    struct AddPointer : TypeIdentity<T *>
    {
    };
    ```
    为最大程度复用代码，应用继承而不是重写`type=...`
    
- 返回传入类型的引用类型，若不能添加引用属性，则返回类型本身
    ```c++
    template <typename T>
    struct AddReference : TypeIdentity<T &>
    {
    };

    template <>
    struct AddReference<void> : TypeIdentity<void>
    {
    };
    ```
    添加引用属性可能会触发引用折叠，感兴趣可以查阅相关资料  
    除了狗void，还有谁不能添加引用呢？

- 输入类型T和一个整数N，输出T的第N层指针
    ```c++
    template <typename T, std::size_t N>
    struct AddNPointer : TypeIdentity<typename AddNPointer<T, N - 1>::type *>
    {
    };
    
    template <typename T>
    struct AddNPointer<T, 0> : TypeIdentity<T>
    {
    };
    ```
- 输入类型T，输出T的指针层数
    ```c++
    template <typename T>
    struct CountPointer
    {
        constexpr static std::size_t value = 0;
    };

    template <typename T>
    struct CountPointer<T *>
    {
        constexpr static std::size_t value = CountPointer<T>::value + 1;
    };
    ```
- 输入若干个类型，输出尺寸最大的类型
    ```c++
    template <bool, typename T1, typename T2>
    struct Conditional : TypeIdentity<T1>
    {
    };

    template <typename T1, typename T2>
    struct Conditional<false, T1, T2> : TypeIdentity<T2>
    {
    };

    template <typename... Args>
    struct MaxSizeOf;

    template <typename T>
    struct MaxSizeOf<T>
        : TypeIdentity<T>
    {
    };

    template <typename T1, typename T2, typename... Args>
    struct MaxSizeOf<T1, T2, Args...>
        : TypeIdentity<typename MaxSizeOf<typename Conditional<(sizeof(T1) > sizeof(T2)), T1, T2>::type,
                                          Args...>::type>
    {
    };
    ```

好了，这次先到这里