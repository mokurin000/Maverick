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

## 关于翻译

[oxa]: https://github.com/oxalica
[xieyuheng]: https://github.com/xieyuheng
[unsafeIO]: https://github.com/unsafeIO
[Edward_P]: https://github.com/edward-p
[Rust 语言术语中英文对照表]: https://rustwiki.org/wiki/translate/english-chinese-glossary-of-rust/
[在仓库中指出]: https://github.com/poly000/poly000.github.io/issue

主要译者：[poly000](https://github.com/poly000)，[比那名居](https://t.me/Hinanawi_Tenshi_M)

参考了这些人（排名不分先后）的建议：[unsafeIO]，[xieyuheng]，[oxa]，[Edward_P]。

术语部分翻译参考了 [Rust 语言术语中英文对照表]，有改动。

如果有翻译错误，请您[在仓库中指出]！

如果有原文错误，请联系 [Ethan Brierley] 且联系我更新翻译。

汉化进度： 480/849 行

## Credits

[原文]: https://lazy.codes/posts/awesome-unstable-rust-features/
[Ethan Brierley]: https://twitter.com/efun_b

[原文] by [Ethan Brierley]

## 简介

这篇文章介绍了一些尚不稳定的 Rust 编译器特性。它将会简要叙述这些特性，并不会深入太多的细节。

## 什么是Unstable Rust？

Rust 发布于三个渠道： stable，beta，以及 nightly。

Nightly 编译器每天都会发布，而且唯有它允许你解锁不稳定 Rust 特性。

> 这篇文章只讨论 Unstable 编译器特性，不稳定的库特性不属于这个话题。

## 为什么要用 Unstable 特性？

[bug tracker]: https://github.com/rust-lang/rust/issues
[Unstable 特性列表]: https://github.com/rust-lang/rust/blob/135ccbaca86ed4b9c0efaf0cd31442eae57ffad7/src/librustc_feature/active.rs#L83-L530
[ICE]: https://github.com/rust-lang/rust/labels/I-ICE

Unstable Rust 可以让你使用在Stable Rust 中无法表示的API。正因如此，编译器与标准库都使用了 Unstable 特性。

使用 Unstable 特性总是伴随着一些风险。它们经常会有一些意想不到的行为，有时甚至会破坏 Rust 的内存安全保证，导致未定义行为。一部分特性可能开发的很好，而另一部分可能未开发完善。

对于使用不稳定特性的 Nightly 编译器，遇到“内部编译器错误”并不少见，这种情况通常称为[ICE]。它发生于编译过程中，编译器将会panic。这可能是由于数据与查询操作因未完成的特性而畸形，甚至可能只是因为未做出的特性部分被打了一个 `todo!()`。

如果你遇到了ICE，检查一下这个问题是否已知，否则就把它报告给[bug tracker]。

Rust 不保证在未来继续支持它的 Unstable 特性。
作为 Rust 开发者，我们享受着优秀的向下兼容性与稳定性，
而启用 Unstable 特性时，这些保证都被抛在脑后。
今天工作的程序可能明天就大不相同。

我决定研究 Unstable 特性，不是因为我需要用它们去解决实际问题。
我寻找它们是因为我觉得他们很有趣。
对我来说，使用 Unstable 的特性，是一种有趣的，使我更多地参与到语言本身的开发过程的方法。

> Unstable 特性的全面列表见[Unstable 特性列表]。

## 启用 Unstable 特性

为了开始使用 Unstable 特性，首先你需要安装 Nightly 工具链：

```bash
rustup toolchain install nightly
```

若要使用 Nightly 工具链，你需要在运行命令时加上 `+nightly` 修饰符。

```bash
<rust-command> +nightly <args>
```

例如：

```bash
cargo +nightly run
```

另外，你可以将你的默认编译器改为 Nightly ，这样你就不再需要使用 `+nightly` 修饰符。
我经常这样做，因为我不认为 nightly 编译器很不稳定，即使对于我的在 stable 上可以编译的项目也是这样。

```bash
rustup default nightly
```

一旦你使用 nightly 编译器，你就可以直接开始使用 Unstable 特性。让我们试一试吧！

```rust
fn main() {
    let my_box = box 5;
}
```

它会导致这样的编译错误：

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

正如以往，Rust 在 `help` 消息中准确地告诉了我们需要做什么。
我们需要用 `#![feature(box_syntax)]` 启用这个特性。

```rust
#![feature(box_syntax)]
fn main() {
    let my_box = box 5;
}
```

所有 Unstable 特性都需要在可以使用前以 `#![feature(..)]` 启用。
如果你忘记了，编译器**通常**会正确地指出要如何做，然而，并非总会这样。

现在，让我们开始讨论一些特性本身。
我把你需要启用的特性名称放在每个特性的标题中的 `代码块` 中，而在代码片段中省略它们，以保持简洁。

## 控制流、模式和块

### `destructuring_assignment`

在Rust中，在绑定某一类型到一个定义时解构它是很常见的。
这通常是通过 `let` 绑定完成的。

```rust
// 创建两个 "变量", 一个是 x, 一个是 y 
let Point { x, y } = Point::random();
```

传统上，这种模式只有在实例化一个新定义时才能实现。
`destructuring_assignment` 将它拓展到可用于修改值时。
<!-- extends this to work when mutating values -->

换句话说，我们可以不使用 `let` 完成解构。

```rust
let (mut x, mut y) = (0, 0);

Point { x, y } = Point::random();
```

### 从任意块提前返回，`label_break_value`

[`loop`可以带值退出]: https://doc.rust-lang.org/edition-guide/rust-2018/control-flow/loops-can-break-with-a-value.html
[关于rust表达式]: https://doc.rust-lang.org/reference/statements-and-expressions.html
[not goto]: http://david.tribble.com/text/goto.html
[标记`loop`]: https://doc.rust-lang.org/rust-by-example/flow_control/loop/nested.html

一个很少被知道的 Rust 特性是，[`loop`可以带值退出]。
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

`label_break_value` 把它拓展到可用于任何被标记的块，而不仅仅是 `loop`。
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

[版本引导]使用这个例子展示问号运算符是如何工作的：

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

使用 `?` 操作符简化代码，可以得到这样等效的代码：

```rust
fn read_username_from_file() -> Result<String, io::Error> {
    let mut f = File::open("username.txt")?;
    let mut s = String::new();

    f.read_to_string(&mut s)?;

    Ok(s)
}
```

`?` 在函数中被用于遇到 `Err` 时提前返回它。
`try_blocks` 解锁了适用于任意代码块而不仅仅是函数的相同功能。
使用 `try_blocks` 我们可以内联我们的 `read_usernames_from_file` 函数。

`try_blocks` 和 `?` 的关系就像是 `label_break_value` 和 `return` 的关系。
`try_blocks` 的RFC提到了 `label_break_value` ，作为一种可能的 `try_blocks` 解读方式。

接写来重写我们的 `read_username_from_file` 成一个简单的 `let` 绑定与一个 `try` 代码块。

```rust
let read_username_from_file: Result<String, io::Error> = try {
    let mut f = File::open("username.txt")?;
    let mut s = String::new();

    f.read_to_string(&mut s)?;

    Ok(s)
}
```

我喜欢这种东西。特别是较小的表达式，如果不提取成函数，易读性会更好。

### `inline_const`

[constant propagation]: https://blog.rust-lang.org/inside-rust/2019/12/02/const-prop-on-by-default.html

目前，获取一个编译时计算的值需要定义一个常量。

> 译者注：或者是 `const fn`

```rust
const PI_APPROX: f64 = 22.0 / 7.0;

fn main() {
     let value = func(PI_APPROX);
}
```

使用 `inline_const` 我们可以用匿名表达式完成同样的事。

```rust
fn main() {
     let value = func(const { 22.0 / 7.0 });
}
```

在这个简单的例子中， `const` 块几乎完全是不必要的，因为编译器的优化[constant propagation]。
然而，对于更复杂的常量，用块来表示可能很有益。

这个特性也允许这些块在模式中使用。
`match x { 1 + 3 => {} }` 会导致格式错误，而 `match x { const { 1 + 3 } => {} }` 不会。

### `if_let_guard`

[if 守卫]: https://doc.rust-lang.org/beta/rust-by-example/flow_control/match/guard.html

拓展可用在 `match` 表达式中的 [`if` 守卫][if 守卫] ，允许使用 `if let`。

> 译注：原文中使用了 "`match` statement" 的说法，这里翻译为 `match` 表达式。

### `let_chains`

目前，`if let` 和 `while let` 表达式不能以 `||` 或 `&&` 连接，
这个特性添加了支持。

## Traits

### `associated_type_bounds`

看看这个稳定 Rust 函数：

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

通过 `associated_type_bounds` 特性，我们可以在这种情况下使用一个匿名类型。

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

使用这个特性，我们可以简单地写成：

```rust
fn flatten_twice<T>(iter: T) -> Flatten<Flatten<T>>
where
    T: Iterator<Item: IntoIterator<Item: IntoIterator>>,
{
    iter.flatten().flatten()
}
```

这对我来说容易推导许多。

### `default_type_parameter_fallback`, `associated_type_defaults`以及`const_generics_defaults`

[泛型类型]: https://github.com/rust-lang/rfcs/blob/master/text/0213-defaulted-type-params.md
[关联类型]: https://github.com/rust-lang/rfcs/blob/master/text/2532-associated-type-defaults.md

这些特性允许你为 [泛型类型], [关联类型] 以及 [const 变量](#const-泛型) 在更多地方指定默认值。

它们允许你作为开发者创建更好的 API 。
如果一个crate的用户对细节不感兴趣，而且那个物件有默认值，可以忽略细节。
它们也让拓展 API 变得容易，无需对你的用户做出破坏性更新。

### `negative_impls` 和 `auto_traits`

[send]: https://doc.rust-lang.org/std/marker/trait.Send.html
[sync]: https://doc.rust-lang.org/std/marker/trait.Sync.html
[send impl]: https://doc.rust-lang.org/src/core/marker.rs.html#38-40

这些特性都被标准库使用。[`Send`][send] 和 [`Sync`][sync] 都是自动 trait 的例子。

`Send` trait 被[这样定义在标准库中][send impl]：

```rust
pub unsafe auto trait Send {
    // 空的
}
```

它让编译器为任意 结构体/枚举/联合 自动实现 `Send` trait，前提是构成这个类型的类型都实现了`Send`。

如果每个类型都能简单地实现 自动trait ，它们也不会那么有用。
这正是引入 `negative_impls` 的原因。

`negative_impls` 允许一个类型选择不实现自动trait。
例如 `UnsafeCell` 。不受限制的 `UnsafeCell` 在线程间共享是非常不安全的，因此它被标记为 `Sync` 也是很不安全的。

```rust
impl<T: ?Sized> !Sync for UnsafeCell<T> {}
```

注意 `!` 创造性的使用，表示 “不`Sync`”。

### `marker_trait_attr`

这个特性为 trait添加了`#[marker]` attribute。

Rust 不允许 the defining of traits implementations that could overlap.
This is so that the compiler will always know which implementation to use because there will always be only one.

Traits marked with `#[marker]` cannot override anything in their implementations.
That way they are allowed to have overlapping implementations because all implementations will be the same.

### `type_alias_impl_trait`, `impl_trait_in_bindings` and `trait_alias`

`impl Trait` tells the compiler to infer a concrete type to replace it with that implements `Trait`.
Currently, `impl Trait` is only used in the context of function arguments or return types.

`type_alias_impl_trait` and `impl_trait_in_bindings` extend the places `impl trait` can be used to include type aliases and `let` bindings respectively.

`trait_alias` is subtlely different to `type_alias_impl_trait`.
Everywhere you use a type alias the type must remain constant.
A single concrete type must be inferred by the compiler that works in all those places.
Trait aliases are more forgiving as they can be a different type in each place they are used.

### `fn_traits` and `unboxed_closures`

[function overloading]: https://en.wikipedia.org/wiki/Function_overloading
[variadic functions]: https://en.wikipedia.org/wiki/Variadic_function

The three traits `Fn`, `FnMut` and `FnOnce` are known as the fn traits.
They are automatically implemented for any functions or closures that you create and are what provides the ability to pass arguments to them.

An automatic implementation is currently the only way to implement those traits.
The `fn_traits` feature allows for custom implementations on any type.
This is very similar to operator overloading but customising the use of `()`.

```rust
#![feature(unboxed_closures)] // required to implement a function with `extern "rust-call"`
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

Notice that this is being used to create a hacky version of [function overloading] and [variadic functions].

## Sugar

### `box_patterns` and `box_syntax`

These two features make constructing and destructing `Box`es easier.
The `box` keyword replaces `Box::new(..)` and allows for the dereferencing `Box`es when pattern matching.

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

Currently to be async inside of a closure you have to use an async block.

```rust
app.at("/").get(|_| async { Ok("Hi") });
```

`async_closure` allows you to mark the closure itself as async just like you would a async function.

```rust
app.at("/").get(async |_| Ok("Hi"));
```

### `in_band_lifetimes`

[how lifetimes used to work]: https://github.com/rust-lang/rfcs/pull/2115#issuecomment-323221054

To use a lifetime it must be explicitly brought into scope.

```rust
fn select<'data>(data: &'data Data, params: &Params) -> &'data Item;
```

With `in_band_lifetimes` the lifetimes can be used without bringing them into scope first.

```rust
fn select(data: &'data Data, params: &Params) -> &'data Item;
```

Interestingly enough this was [how lifetimes used to work] pre `1.0.0`.

### `format_args_capture`

This allows for named arguments to be placed inside of strings inside any macro that depends on `std::format_args!`.
That includes `print!`, `format!`, `write!` and many more.

```rust
let name = "Ferris";
let age = 11;
println!("Hello {name}, you are {age} years old");
```

It is likely that this will be stabilised with or soon after edition 2021.

### `crate_visibility_modifier`

With this feature you can write `crate struct Foo` rather than `pub(crate) struct Foo` and have it mean exactly the same thing.

This makes `pub(crate)` easier to write, encouraging the use of crate visibility when full `pub` is not necessary.

## Types

### `type_ascription`

Take for example the `collect` method on `Iterator`.
Collect transforms an interator into a collection.

```rust
let word = "hello".chars().collect();
println!("{:?}", word);
```

This does not compile because Rust is unable to infer the type of `word`.
This can be fixed by replacing the first line with:

```rust
let word: Vec<char> = "hello".chars().collect();
```

With `type_ascription` the `let` binding is no longer necessary and one can simply:

```rust
println!("{:?}", "hello".chars().collect(): Vec<char>);
```

The `: Type` syntax can be used anywhere to hint at the compiler "I want this type at this point".

### `never_type`

It is possible to define `enum`s with zero variants.
Such an enum exists stable in the standard library.

```rust
pub enum Infallible {}
```

It is possible to use this type in generics and function signatures but never possible for it to be constructed.
There are simply no variants to construct.

The unit type, `()` would be equivalent to an enum with a single variant.
`never_type` introduces a new type, `!` which is equivalent to our `Infallible` enum with zero variants.

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

这个功能让你几乎可以在任何地方放置属性，而不仅仅是顶层项目。例如，有了这个功能，你就可以在一个闭包上放置一个[optimize attribute](#optimize-attribute)

### `cfg_version`

该功能允许根据编译器版本进行条件编译。

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

[impossible to write anything useful]: https://github.com/rust-lang/rust/issues/29639#issuecomment-155280578

自从你可以用 `#![no_std]` 选项来选择不使用标准库已经过了一段时间了。
这对于不在完整环境中运行的应用非常重要，比如嵌入式系统。
嵌入式系统通常没有操作系统，甚至没有动态内存，所以 `std` 中的许多功能都无法使用。

更进一步的，你现在可以通过 `#![no_core]` 选项来选择不使用 libcore。
这会几乎不给你留下任何东西，你甚至不能使用libc。
这会让你[很难实现任何有用的东西][impossible to write anything useful]。

## 其它

### Const 泛型

> 这个小节由 [@Hinanawi_Tenshi_M](https://t.me/Hinanawi_Tenshi_M) 提供翻译，有改动。

[rust dublin talk]: https://lazy.codes/posts/intro-to-const-generics/

我在都柏林 Rust 集会中做过一个关于 const_generics 的未来的[演讲][rust dublin talk]。
与其重复那些内容，我更推荐大家去[看这个演讲][rust dublin talk]。

## Macros 2.0

Rust's declarative macros are very powerful however some of the rules around `macro_rules!` have always confused me.

For one, `macro_rules!` acts as a simple token transformation.
It takes a list of tokens and outputs a new list of tokens, nothing smarter than that.
The publicity rules end up being the rules of where the macro is being called.
This is obvious because the codes is being simply pasted into that place.

Macros 2.0 is an rfc describing a replacement to `macro_rules!` with a new construct simply using the keyword `macro`.

One of the main improvements the new syntax introduces is macro hygiene which allows macros to use the publicity rules of where they are written rather than where they are called.

### `generators`

Generators/coroutines provide a special kind of function that can be paused during execution to "yield" intermediate values to the caller.

Generators can return multiple values using the `yield` keyword, each time pausing the function and returning to the caller.
A generator can then `return` a single value after which it can no longer be resumed.

About three years ago I attempted to write an algorithm to traverse an infinite matrix along its diagonals.
I found it very difficult to write that with Rust's iterators and ended up giving up.

Here is an implementation using Rust's generators/coroutines along with a number of other features we've discussed already.

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

Generators make it possible to write implementations that are far more difficult or even impossible to write without them.

Generators were added to implement async-await in the standard library.
It is most likely that the exact semantics will change before any kind of stabilisation but they are very fun to play with.

### Final thoughts

[Generic associated types]: https://github.com/rust-lang/rfcs/blob/master/text/1598-generic_associated_types.md
[inline asm]: https://rust-lang.github.io/rfcs/2873-inline-asm.html
[specialization]: https://rust-lang.github.io/rfcs/1210-impl-specialization.html
[Twitter]: https://twitter.com/efun_b
[RFC]: https://rust-lang.github.io/rfcs/
[tracking issue]: https://github.com/rust-lang/rust/labels/C-tracking-issue
[the unstable book]: https://doc.rust-lang.org/beta/unstable-book/the-unstable-book.html

I have to apologise for not including three amazing unstable features; [Generic associated types], [inline asm] and [specialization].
I simply did not feel able to give these features justice in this article but I may try to talk about them in future.

If you wish to read more about an unstable feature the best place to start is [the unstable book] where most of them are listed.
The unstable book then links to a [tracking issue] which then often, in turn, links to an [RFC].
With this combination of sources, you can then build up a picture of the details surrounding a feature.

Thank you for reading my first blog post 😃.
The best way to support me is by following my [Twitter].
I am also looking for employment opportunities so please get in touch if you would like to talk about that.
