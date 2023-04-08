---
layout: post
title: 一些不错的Rust Unstable特性
slug: awesome-unstable-rust-features
date: 2021-07-28 15:04
status: publish
author: Poly000
categories: 
  - Programming
tags: 
  - Rust
  - Language_feature
---

## 注意

本文原文发布于2021-07-26，其中部分内容可能已经过时。请以 Rust RFC 为准。
已经稳定的特性见 [accepted.rs](https://github.com/rust-lang/rust/blob/master/compiler/rustc_feature/src/accepted.rs)。

## 关于翻译

[Rust 语言术语中英文对照表]: https://rustwiki.org/wiki/translate/english-chinese-glossary-of-rust/

主要译者：[poly000](https://github.com/poly000)，[比那名居](https://t.me/Hinanawi_Tenshi_M)

术语翻译部分参考了 [Rust 语言术语中英文对照表]。

如果有原文错误，请联系 [Ethan Brierley] 且联系我更新翻译。

参与：[Maverick/demo_src](https://github.com/poly000/Maverick/)

## Credits

[原文]: https://lazy.codes/posts/awesome-unstable-rust-features/
[Ethan Brierley]: https://twitter.com/efun_b

[原文] by [Ethan Brierley]

## 简介

这篇文章介绍了一些尚不稳定的 Rust 编译器特性。我将会简单叙述这些特性，并不会深入太多细节。

## 什么是Unstable Rust？

Rust 有三个发布版本： stable，beta，nightly。

Nightly 编译器每天都会发布，而且只有它允许你启用 Unstable Rust 特性。

> 这篇文章只讨论 Unstable 编译器特性，不讨论此版本的标准库特性。

## 为什么要用 Unstable 特性？

[bug tracker]: https://github.com/rust-lang/rust/issues
[Unstable 特性列表]: https://github.com/rust-lang/rust/blob/135ccbaca86ed4b9c0efaf0cd31442eae57ffad7/src/librustc_feature/active.rs#L83-L530
[ICE]: https://github.com/rust-lang/rust/labels/I-ICE

Unstable Rust 可以让你使用在Stable Rust 中不允许使用的API。为此，编译器与标准库都使用了 Unstable 特性。

使用 Unstable 特性总是伴随着一些风险。它们经常会有一些不期望行为，有时甚至会破坏 Rust 的内存安全保证，导致未定义行为。这些特性可能开发的很好，但也能未开发完善。

使用Unstable特性的 Nightly 编译器，遇到“内部编译器错误”并不少见，这种情况通常称为[ICE]。它发生于编译过程中，编译器将会panic。这可能是由于数据与查询操作因未完成的特性而被破坏，甚至可能只是因为没做完的特性中打了个 `todo!()`。

如果你遇到了ICE，检查一下是否已经被反馈，没有的话就把它报告给[bug tracker]。

Rust 不保证在未来继续支持它的 Unstable 特性。
作为 Rust 开发者，我们享受着优秀的向下兼容性与稳定性，
而启用 Unstable 特性时，Rust不再提供这些保证。
今天工作的程序可能明天就寄了！

我决定学习 Unstable 特性，不是因为我需要用它们去解决实际问题，而是觉得他们很有趣。
对我来说，使用 Unstable 特性，是种有趣的让我更多地参与语言本身的开发过程的方法。

> Unstable 特性的完整列表见[Unstable 特性列表]。

## 启用 Unstable 特性

为了使用 Unstable 特性，首先你需要安装 Nightly 工具链：

```bash
rustup toolchain install nightly
```

临时使用 Nightly 工具链，你可以在运行cargo时加上 `+nightly`。

```bash
<rust-command> +nightly <args>
```

例如：

```bash
cargo +nightly run
```

另外，你可以将你的默认编译器改为 Nightly ，这样你就不再需要加上 `+nightly。

```bash
rustup default nightly
```

切换到 nightly 编译器后，你就可以使用 Unstable 特性。让我们试一试吧！

```rust
fn main() {
    let my_box = box 5;
}
```

你会得到如下编译错误：

```rust
error[E0658]: box expression syntax is experimental; you can call `Box::new` instead
 --> src/main.rs:2:18
  |
2 |     let my_box = box 5;
  |                  ^^^^^
  |
  = note: see issue #49733 <https://github.com/rust-lang/rust/issues/49733> for more information
  = help: add `#![feature(box_syntax)]` to the crate attributes to enable
```

Rust 在 `help` 消息中准确地告诉了我们应该做什么——
我们需要用 `#![feature(box_syntax)]` 启用这个特性。

```rust
#![feature(box_syntax)]
fn main() {
    let my_box = box 5;
}
```

所有 Unstable 特性都需要用 `#![feature(..)]` 启用。
即使你忘记了，编译器通常也会指出要如何做，虽然不总会是。

现在，我们看看这些特性。
我把需要启用的特性名称放在每个特性的标题中的 `代码块` 中，在代码片段中省略，以保持简洁。

## 控制流、模式和块

### `destructuring_assignment`

> 于 Rust 1.59 稳定。

在Rust中，我们经常在绑定到定义时解构某个类型。
我们一般会使用`let`绑定：

```rust
// 创建两个变量, 一个是 x, 一个是 y 
let Point { x, y } = Point::random();
```

目前这种写法只得在实例化新的定义时使用。
`destructuring_assignment` 将它拓展到赋值。

换句话说，我们可以不使用 `let` 完成解构。

```rust
let (mut x, mut y) = (0, 0);

Point { x, y } = Point::random();
```

### 从任意块提前返回，`label_break_value`

> 于 Rust 1.65 稳定。

[`loop`可以带值退出]: https://doc.rust-lang.org/edition-guide/rust-2018/control-flow/loops-can-break-with-a-value.html
[关于rust表达式]: https://doc.rust-lang.org/reference/statements-and-expressions.html
[not goto]: http://david.tribble.com/text/goto.html
[标记`loop`]: https://doc.rust-lang.org/rust-by-example/flow_control/loop/nested.html

Rust 有一个不那么广为人知的特性，[`loop`可以带值退出]。
就像 Rust 中许多其它的结构，在 Rust 中 `loop` 并不仅仅是语句, 而是[表达式][关于rust表达式]。

```rust
// 保持请求用户输入一个数字，直到他们给出一个有效的数字。
let number: u8 = loop {
    if let Ok(n) = input().parse() {
        break n;
    } else {
        println!("Invaid number, Please input a valid number");
    }
};
```

`label_break_value` 把这拓展到任何被标记的块，而不仅仅是 `loop`。
它的行为，就像是一种提前的 `return` ，不过适用于任何代码块，而不只是函数体。

标记代码块的语法，和生命周期很相似。

```rust
'block: {
     // 这个代码块现在被标记为 "block" 。
}
```

现在也可以用同样的方式[标记`loop`]。

我们可以把标签放在 `break` 后面，从那个代码块提前返回。

```rust
let number = 'block: {
    if s.is_empty() {
      break 'block 0; // 从代码块提前返回
    }
    s.parse().unwrap()
}
```

> 这个特性[不等价于goto][not goto]。
> 它没有 goto 那样的破坏性影响，他只是往后继续执行，从一个代码块中退出。

### 使用 `try_blocks` 内联 `?` 操作符的功能

[版本引导]: https://doc.rust-lang.org/edition-guide/rust-2018/error-handling-and-panics/the-question-mark-operator-for-easier-error-handling.html

[版本引导]用这个例子解释问号运算符的工作方式：

```rust
fn read_username_from_file() -> Result<String, io::Error> {
    let f = File::open("username.txt");

    let mut f = match f {
        Ok(file) => file,
        Err(e) => return Err(e),
    };

    let mut s = String::new();

    match f.read_to_string(&mut s) {
        Ok(_) => Ok(s),
        Err(e) => Err(e),
    }
}
```

使用 `?` 操作符简化，可以得到等效的代码：

```rust
fn read_username_from_file() -> Result<String, io::Error> {
    let mut f = File::open("username.txt")?;
    let mut s = String::new();

    f.read_to_string(&mut s)?;

    Ok(s)
}
```

`?` 可以在函数中提前返回 `Err`。
`try_blocks` 提供了适用于任意代码块的相同功能。
使用 `try_blocks` ，我们可以内联 `read_usernames_from_file` 函数。

`try_blocks` 和 `?` 的关系就像是 `label_break_value` 和 `return` 的关系。
`try_blocks` 的RFC提到了 `label_break_value` ，作为 `try_blocks` 一种可能的解糖。

接下来重写我们的 `read_username_from_file` ，
我们得到了一个简单的 `let` 绑定和 `try` 代码块。

```rust
let read_username_from_file: Result<String, io::Error> = try {
    let mut f = File::open("username.txt")?;
    let mut s = String::new();

    f.read_to_string(&mut s)?;

    Ok(s)
}
```

我喜欢这个特性。特别是对于较小的表达式，如果不提取成函数，可读性会更好。

### `inline_const`

[constant propagation]: https://blog.rust-lang.org/inside-rust/2019/12/02/const-prop-on-by-default.html

目前，指定某个值编译时计算需要定义一个常量。

```rust
const PI_APPROX: f64 = 22.0 / 7.0;

fn main() {
     let value = func(PI_APPROX);
}
```

有了 `inline_const` 我们可以用匿名表达式完成同样的事。

```rust
fn main() {
     let value = func(const { 22.0 / 7.0 });
}
```

在这个简单的例子中， 因为编译器优化[constant propagation]，`const` 块几乎可以说是不必要的。
但是对于更复杂的常量，用块来表示可能更好。

这个特性也允许在模式匹配中使用const块。
如 `match x { 1 + 3 => {} }` 会导致语法错误，而 `match x { const { 1 + 3 } => {} }` 不会。

### `if_let_guard`

[if 守卫]: https://doc.rust-lang.org/beta/rust-by-example/flow_control/match/guard.html

拓展 `match` 中的 [`if` 守卫][if 守卫] ，使其允许使用 `if let`。

### `let_chains`

> 于 Rust 1.64 稳定。

目前，`if let` 和 `while let` 表达式不能以 `||` 或 `&&` 连接，
这个特性添加了支持。

## Traits

### `associated_type_bounds`

看看这个 stable Rust 函数：

```rust
fn fizzbuzz() -> impl Iterator<Item = String> {
    (1..).map(|val| match (val % 3, val % 5) {
        (0, 0) => "FizzBuzz".to_string(),
        (0, _) => "Fizz".to_string(),
        (_, 0) => "Buzz".to_string(),
        (_, _) => val.to_string(),
    })
}
```

有了 `associated_type_bounds` 特性，我们可以在这种情况下使用一个匿名类型：

```rust
fn fizzbuzz() -> impl Iterator<Item: Display> { ... }
```

看看这个吓人地冗长的类型签名：

```rust
fn flatten_twice<T>(iter: T) -> Flatten<Flatten<T>>
where
    T: Iterator,
    <T as Iterator>::Item: IntoIterator,
    <<T as Iterator>::Item as IntoIterator>::Item: IntoIterator,
{
    iter.flatten().flatten()
}
```

有了这个特性，我们就可以简单地写成：

```rust
fn flatten_twice<T>(iter: T) -> Flatten<Flatten<T>>
where
    T: Iterator<Item: IntoIterator<Item: IntoIterator>>,
{
    iter.flatten().flatten()
}
```

这种写法容易理解许多。

### `default_type_parameter_fallback`, `associated_type_defaults`以及`const_generics_defaults`

[泛型类型]: https://github.com/rust-lang/rfcs/blob/master/text/0213-defaulted-type-params.md
[关联类型]: https://github.com/rust-lang/rfcs/blob/master/text/2532-associated-type-defaults.md

> `const_generics_defaults` 于 Rust 1.59 稳定。

这些特性允许你为 [泛型类型], [关联类型] 以及 [const 变量](#const-泛型) 在更多地方指定默认值。

它们允许你作为开发者创建更好的 API 。
如果一个crate的用户对细节不感兴趣，而它有默认值，则可以忽略细节。
这也让拓展 API 变得容易，无需做出破坏性更新。

### `negative_impls` 和 `auto_traits`

[send]: https://doc.rust-lang.org/std/marker/trait.Send.html
[sync]: https://doc.rust-lang.org/std/marker/trait.Sync.html
[send impl]: https://doc.rust-lang.org/src/core/marker.rs.html#38-40

这些特性都被标准库使用。[`Send`][send] 和 [`Sync`][sync] 都是自动 trait。

`Send` trait 被[这样定义在标准库中][send impl]：

```rust
pub unsafe auto trait Send {
    // 空的
}
```

注意`auto`关键字，它让编译器为任意结构体/枚举体/联合体自动实现 `Send` trait，（前提是构成这个类型的类型都实现了`Send`）

如果每个类型都能简单地实现自动trait ，它们也不会那么有用。
这正是引入 `negative_impls` 的原因。

`negative_impls` 允许一个类型不实现某个auto trait。
举个例子，`UnsafeCell`。不受限制的 `UnsafeCell` 在线程间共享非常不安全，因此它被标记为 `Sync` 也不安全。

```rust
impl<T: ?Sized> !Sync for UnsafeCell<T> {}
```

注意 `!` ，表示 “不`Sync`”。

### `marker_trait_attr`

这个特性为 trait 添加了`#[marker]` 属性。

> 详见 [Unstable Book](https://doc.rust-lang.org/beta/unstable-book/language-features/marker-trait-attr.html)

Rust 不允许定义trait的实现时覆盖此前的实现。
这样编译器就能确定要使用哪个实现——只有一个。

标志为 `#[marker]` 的 trait 不能在实现中覆盖任何东西。
这样它们就能允许重叠的实现，因为所有的实现都是一样的。

### `type_alias_impl_trait`, `impl_trait_in_bindings` and `trait_alias`
`impl Trait` 让编译器推导具体类型，把它换成实现了`Trait`的类型。
目前，`impl Trait`只能在函数参数或返回类型中使用，无法应用于变量绑定。

> 注：impl_trait_in_binding 临时被移除(2022-07-26)，可能是因为[破坏性更新](https://github.com/rust-lang/rust/issues/83021)
`type_alias_impl_trait` 和 `impl_trait_in_bindings` 拓展了 `impl trait`，让其可用于定义类型别名和 `let` 绑定。

`trait_alias` 与 `type_alias_impl_trait` 有微妙的不同：
你使用类型别名的时候，类型必须是固定的。
编译器必须推断出，并且只应用单一具体的类型。
trait别名则较为宽松，每次使用都可以是不同的类型。

### `fn_traits` and `unboxed_closures`

[函数重载]: https://en.wikipedia.org/wiki/Function_overloading
[不定参函数]: https://en.wikipedia.org/wiki/Variadic_function

`Fn`，`FnMut`和`FnOnce`被认为是`fn`的trait。
它们会被任何函数或者你创建的闭包自动实现，它们允许你给它们传参。

目前它们只能被自动实现。
`fn_trait` 则允许为任意类型提供自定义实现。
这就像是操作符重载，但要自定义的是`()`调用。

```rust
#![feature(unboxed_closures)] // 实现带有`extern "rust-call"`的函数
#![feature(fn_traits)]

struct Multiply;

#[allow(non_upper_case_globals)]
const multiply: Multiply = Multiply;

impl FnOnce<(u32, u32)> for Multiply {
    type Output = u32;
    extern "rust-call" fn call_once(self, a: (u32, u32)) -> Self::Output {
        a.0 * a.1
    }
}

impl FnOnce<(u32, u32, u32)> for Multiply {
    type Output = u32;
    extern "rust-call" fn call_once(self, a: (u32, u32, u32)) -> Self::Output {
        a.0 * a.1 * a.2
    }
}

impl FnOnce<(&str, usize)> for Multiply {
    type Output = String;
    extern "rust-call" fn call_once(self, a: (&str, usize)) -> Self::Output {
        a.0.repeat(a.1)
    }
}

fn main() {
    assert_eq!(multiply(2, 3), 6);
    assert_eq!(multiply(2, 3, 4), 24);
    assert_eq!(multiply("hello ", 3), "hello hello hello ");
}
```

这可被用于实现有点 hacky 的[函数重载]和[不定参函数].

## 语法糖

### `box_patterns` and `box_syntax`

这两个特性让`Box`的构造和析构变得更容易。
box关键字将取代`Box::new(...)`，并且允许在模式匹配中解引用`Box`。

```rust
struct TrashStack<T> {
    head: T,
    body: Option<Box<TrashStack<T>>>,
}

impl<T> TrashStack<T> {
    pub fn push(self, elem: T) -> Self {
        Self {
            head: elem,
            body: Some(box self),
        }
    }

    pub fn peek(self) -> Option<T> {
        if let TrashStack {
            body: Some(box TrashStack { head, .. }),
            ..
        } = self
        {
            Some(head)
        } else {
            None
        }
    }
}
```

> 正如原文作者所说，rust（包括内部实现）正在减少box syntax的使用。
> 所以这个章节咕了（理直气壮）

This makes things a little more ergonomic but I don't think there is much chance that this feature will ever be stabilised.
It seems to have existed forever with no plan for stabilisation but instead a little discussion about removing the feature.
`box_synatx` is used heavily in the compiler's source and a little in the standard library.

It is interesting to note that `box` does not desugar to `Box::new` but `Box::new` is implemented in the standard library with `box`.

```rust
impl<T> Box<T> {
    ...
    pub fn new(x: T) -> Self {
        box x
    }
    ...
}
```

### `async_closure`

目前在闭包中使用异步代码你需要加async块。

```rust
app.at("/").get(|_| async { Ok("Hi") });
```

`async_closure` 允许你将闭包本身标记为异步的，像异步函数那样写

```rust
app.at("/").get(async |_| Ok("Hi"));
```

### `in_band_lifetimes`

[生命周期]: https://github.com/rust-lang/rfcs/pull/2115#issuecomment-323221054

To use a lifetime it must be explicitly brought into scope.

```rust
fn select<'data>(data: &'data Data, params: &Params) -> &'data Item;
```

With `in_band_lifetimes` the lifetimes can be used without bringing them into scope first.

```rust
fn select(data: &'data Data, params: &Params) -> &'data Item;
```

有趣的是这正是[生命周期]在rust `1.0.0`前的写法。

### `format_args_capture`

> 于 Rust 1.58 稳定。

This allows for named arguments to be placed inside of strings inside any macro that depends on `std::format_args!`.
That includes `print!`, `format!`, `write!` and many more.

```rust
let name = "Ferris";
let age = 11;
println!("你好{name}，你{age}岁了。");
```

### `crate_visibility_modifier`

这个特性允许你写 `crate struct Foo` 而不是 `pub(crate) struct Foo` ，语义不变。

这使得 `pub(crate)` 更易编写，鼓励在pub不必要的时候使用crate可见性，

## Types

### `type_ascription`

用`Iterator`的`collect`方法举个例子：
collect将迭代器转换到集合

```rust
let word = "hello".chars().collect();
println!("{:?}", word);
```

这个不能编译，因为rust无法推导出`word`的类型。
可以把第一行换成：

```rust
let word: Vec<char> = "hello".chars().collect();
```

有了`type_ascription`就不需要再加上let绑定，我们可以直接：

```rust
println!("{:?}", "hello".chars().collect(): Vec<char>);
```

`: Type` 语法可以用在任何一处，提醒编译器“我在这里想要得到这个类型”

### `never_type`

你可以定义没有变体的枚举体，
这种枚举体也存在于标准库中。

```rust
pub enum Infallible {}
```

你可以在泛型或函数签名中使用该类型，但它不可能被构造。
没有可以用来构造的变体。

The unit type, `()` would be equivalent to an enum with a single variant.
元类型，`()` 等价于只有一个变体的枚举。
`never_type` 引入了一种新的类型，`!`等价于我们的没有变体的 `Infallible`。

Because `!` can never be constructed it can be given special powers.
We don't have to handle the case of `!` because we have proven it will never exist.

```rust
fn main() -> ! {
    loop {
        println!("Hello, world!");
    }
}
```

Loops without a `break` "return `!`" because they don't ever return.

`!` can be very useful for expressing impossible outcomes in the type system.
Take for example the `FromStr` implementation on this `UserName` type.
This implementation is infallible because its implementation can never fail.
This allows us to set the `Err` variant to type `!`.

```rust
struct UserName(String);

impl FromStr for UserName {
    type Err = !;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self(s.to_owned()))
    }
}
```

It is then possible to use an empty `match` on the `Err` variant because `!` has no variants.

```rust
let user_name = match UserName::from_str("ethan") {
    Ok(u) => u,
    Err(e) => match e {},
};
```

### `exhaustive_patterns`

With the feature `exhaustive_patterns` the type system becomes smart enough for us to eliminate the `Err` branch altogether.

```rust
let user_name = match UserName::from_str("ethan") {
    Ok(u) => u,
};
```

We can combine this with destructuring to remove the `match` leaving a beautiful line of code.

```rust
let Ok(user_name) = UserName::from_str("ethan");
```

## attribute

> 这个小节由 [@Hinanawi_Tenshi_M](https://t.me/Hinanawi_Tenshi_M) 提供翻译，有改动

### `optimize_attribute`

[opt-level]: https://doc.rust-lang.org/book/ch14-01-release-profiles.html
[web assembly]: https://webassembly.org/

你可以用 `Cargo.toml` 的 [`opt-level`][opt-level] 选项指定你想要怎么优化你的二进制文件。

`opt-level` 指定的是整个 crate 的优化方式，如果你想要分别控制每一个项目的优化方式，你可以使用 `optimize_attribute` 选项。

```rust
#[optimize(speed)]
fn fast_but_large() {
     ...
}

#[optimize(size)]
fn slow_but_small() {
     ...
}
```

这对微调应用程序非常有用，在这些应用程序中，尺寸和性能之间的权衡特别明显，例如在使用 [web assembly] 时。

### `stmt_expr_attributes`

这个特性让你可以在几乎任何地方标记属性，而不仅仅是顶层项目。例如，你可以在一个闭包上放一个[optimize attribute](#optimize-attribute)

### `cfg_version`

该特性允许根据编译器版本进行条件编译。

```rust
#[cfg(version("1.42"))] // 1.42 以上
fn a() {
    // ...
}

#[cfg(not(version("1.42")))] // 1.41 以下
fn a() {
    // ...
}
```

这使得你的 crate 能够使用最新的编译器功能，同时仍然保持对旧编译器的后备支持。

### `no_core`

不使用标准库的 `#![no_std]` 选项已经存在有段时间了。

这对于不在完整环境中运行的应用非常重要，比如嵌入式系统。
嵌入式系统通常没有操作系统，甚至没有动态内存，所以 `std` 中的许多功能都无法使用。

更进一步的，你现在可以通过 `#![no_core]` 选项来选择不使用 libcore。
这会几乎不给你留下任何东西，你甚至不能使用libc。
（比如说，你希望你的crate可以成为libcore的依赖。）

## 其它

### Const 泛型

> 这个小节由 [@Hinanawi_Tenshi_M](https://t.me/Hinanawi_Tenshi_M) 提供翻译，有改动。

[rust dublin talk]: https://lazy.codes/posts/intro-to-const-generics/

我在都柏林 Rust 集会中做过一个关于 const_generics 的未来的[演讲][rust dublin talk]。
与其重复那些内容，我更推荐大家去[看这个演讲][rust dublin talk]。

## Macros 2.0

Rust的声明式宏非常强大，然而有些 `macro_rules!` 的规则让我很困惑。

比如，`macro_rules!`是一个简单的token转换过程。
它接受一个token列表，输出新的token列表，仅仅如此。
可见性原则会遵从宏的调用处的规则。
这很显然——因为代码只是被简单地粘贴回原处。

Macros 2.0 是一个 RFC，介绍了`macro_rules!`的一种替代，它的构造只需要简单地使用关键字`macro`

它的主要改进中，引入了一种新的格式（macro hygiene），允许宏使用它们定义处的可见性规则，而不是调用处。

### `generators`

生成器（协程）提供了一种特殊的函数，可以在执行过程中暂停，“yield” 中间值给调用者。

生成器允许你使用`yield`关键字返回多个值，每次暂停该函数并返回给调用者。

生成器中也可以`return`单个值，不可再恢复。

大约三年前，我尝试编写算法，沿对角线遍历一个无穷的矩阵。我发现用Rust的迭代器编写它非常困难，最终放弃了。

这是我的实现，使用了Rust的生成器（协程）和一些我们刚刚讨论过的特性。

```rust
#![feature(
    try_blocks,
    generators,
    generator_trait,
    associated_type_bounds,
    type_ascription
)]

use std::{
    iter,
    ops::{Generator, GeneratorState},
    pin::Pin,
};

/// Input
/// [[1, 2, 3]
/// ,[4, 5, 6]
/// ,[7, 8, 9]]
/// Output
/// [1, 2, 4, 3, 5, 7]
fn diagonalize<T>(
    mut matrix: impl Iterator<Item: Iterator<Item = T>>,
) -> impl Generator<Yield = T, Return = ()> {
    move || {
        let mut rows = Vec::new();
        (try {
            rows.push(matrix.next()?);
            for height in 0.. {
                for row in 0..height {
                    if row >= rows.len() {
                        rows.push(matrix.next()?);
                    }
                    yield rows[row].next()?;
                }
            }
        }): Option<()>;
    }
}

fn main() {
    let matrix = (0..).map(|x| iter::once(x).cycle().enumerate());
    let mut diagonals = diagonalize(matrix);
    while let GeneratorState::Yielded(value) = Pin::new(&mut diagonals).resume(()) {
        dbg!(value);
    }
}
```

> It is understandable if you found the above snippet hard to interpret.
> It makes use of a number of features that you may have just been introduced to.
>
> There is a compelling argument against adding too many new features as they can greatly increase the learning curve.

生成器让一些没有这个特性会难以编写甚至无法编写的实现变为可能。

生成器在标准库中是为了实现 async/await 添加的。
具体的语义在稳定化前很可能被修改，但它很有趣。

### 总结

[GAT]: https://github.com/rust-lang/rfcs/blob/master/text/1598-generic_associated_types.md
[内联汇编]: https://rust-lang.github.io/rfcs/2873-inline-asm.html
[特化]: https://rust-lang.github.io/rfcs/1210-impl-specialization.html
[Twitter]: https://twitter.com/efun_b
[RFC]: https://rust-lang.github.io/rfcs/
[tracking issue]: https://github.com/rust-lang/rust/labels/C-tracking-issue
[the unstable book]: https://doc.rust-lang.org/beta/unstable-book/the-unstable-book.html

我很抱歉，没有引用另外三个不错的unstable特性：[GAT], [内联汇编]和[特化]。
我只是感觉在这篇文章我做不到客观的评价它们，不过将来我可能会尝试。

如果你想了解更多unstable特性，我推荐你看[the unstable book]，这里会列出绝大部分。
Unstable book会连接到[tracking issue]，而后者往往会链接到[RFC]。
组合使用这些来源，你可以很好地了解新特性。

Thank you for reading my first blog post 😃.
The best way to support me is by following my [Twitter].
I am also looking for employment opportunities so please get in touch if you would like to talk about that.
