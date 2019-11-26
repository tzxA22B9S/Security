<font size=5>@id1e's Hello World</font>

***

<!-- TOC -->

- [Perface](#perface)
- [Web Security](#web-security)
  - [Basic knowledge](#basic-knowledge)
    - [Same Origin Policy (同源策略 SOP)](#same-origin-policy-%e5%90%8c%e6%ba%90%e7%ad%96%e7%95%a5-sop)
      - [**0x00 什么是同源策略？**](#0x00-%e4%bb%80%e4%b9%88%e6%98%af%e5%90%8c%e6%ba%90%e7%ad%96%e7%95%a5)
      - [**0x01 如何判断同源？**](#0x01-%e5%a6%82%e4%bd%95%e5%88%a4%e6%96%ad%e5%90%8c%e6%ba%90)
      - [**0x02 同源策略究竟限制了什么？**](#0x02-%e5%90%8c%e6%ba%90%e7%ad%96%e7%95%a5%e7%a9%b6%e7%ab%9f%e9%99%90%e5%88%b6%e4%ba%86%e4%bb%80%e4%b9%88)
      - [**0x03 如何跨域？**](#0x03-%e5%a6%82%e4%bd%95%e8%b7%a8%e5%9f%9f)
    - [Content Security Policy (内容安全策略 CSP)](#content-security-policy-%e5%86%85%e5%ae%b9%e5%ae%89%e5%85%a8%e7%ad%96%e7%95%a5-csp)
  - [SQL injection (SQL注入)](#sql-injection-sql%e6%b3%a8%e5%85%a5)
  - [Crossing Site Script (跨站脚本 XSS)](#crossing-site-script-%e8%b7%a8%e7%ab%99%e8%84%9a%e6%9c%ac-xss)
  - [Cross Site Request Forgery (跨站请求伪造 CSRF)](#cross-site-request-forgery-%e8%b7%a8%e7%ab%99%e8%af%b7%e6%b1%82%e4%bc%aa%e9%80%a0-csrf)

<!-- /TOC -->

***

## Perface

知识汇总，包括日常学习中遇到的各种值得记录的问题，再此整理。

***

## Web Security


***

### Basic knowledge

> 基础知识整理

***

#### Same Origin Policy (同源策略 SOP)

##### **0x00 什么是同源策略？**  

同源策略是Web应用程序的一种安全**模型**，它控制了网页中DOM之间的访问。

##### **0x01 如何判断同源？**

给定一个页面，如果另一个页面使用的**协议**、**端口**、**主机**都相同，我们则认为两个页面具有相同的源。

##### **0x02 同源策略究竟限制了什么？**

同源策略没有禁止脚本的执行，而是**禁止读取HTTP回复**。

同源策略其实在防止CSRF上作用非常有限，CSRF的请求往往在发送出去的那一瞬间就已经达到了攻击的目的，比如发送了一段敏感数据，或请求了一个具体的功能，是否能读取回复并不那么重要（唯一的作用是可以防止CSRF请求读取异源的授权Token）。 另外，一般静态资源通常不受同源策略限制，如js/css/jpg/png等。

##### **0x03 如何跨域？**

- 通过jsonp跨域 (静态资源获取)
- document.domain (主域相同，子域不同)
- location.hash (A——>B——>C)
- windown.name (name值在不同域名加载后依旧存在)
- postMessage跨域
- nginx代理跨域

***
#### Content Security Policy (内容安全策略 CSP)

### SQL injection (SQL注入)

### Crossing Site Script (跨站脚本 XSS)

### Cross Site Request Forgery (跨站请求伪造 CSRF)

***