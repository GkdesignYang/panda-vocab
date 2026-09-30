# 第三方数据与许可说明

本项目的代码（`index.html`、`tools/build_books.py`）以 MIT 许可发布，见 [LICENSE](LICENSE)。
`books/` 目录里的词库是从下列第三方来源整理、改写而来的，分别遵循各自的许可或版权声明。

| 词库文件 | 来源 | 许可 |
|---|---|---|
| `junior.json` `senior.json` `cet4.json` `cet6.json` `toefl.json` `sat.json` | [KyleBing/english-vocabulary](https://github.com/KyleBing/english-vocabulary) | BSD 3-Clause |
| `ielts.json`（单词表、释义、音标） | [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT) 中标记为 `ielts` 的词条 | MIT |
| 所有词库的音标、`pet.json` 的释义 | [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT) | MIT |
| `pet.json` 的单词表、`tools/pet_words.txt` | Cambridge English《B1 Preliminary Vocabulary List》 | © Cambridge University Press & Assessment，见下文说明 |

改写内容包括：合并重复词条，去掉人名、地名义项，截取简短释义，统一词性与音标写法。

## 剑桥 B1 Preliminary 词表

`tools/pet_words.txt` 只收录了剑桥官方公开的 B1 Preliminary（PET）词表中的单词本身，没有收录原表的例句和分类；中文释义全部来自 ECDICT。
原词表版权属于 Cambridge University Press & Assessment，原文件没有写明转载许可。本项目仅将其用于非商业的学习用途。
如果版权方提出异议，删掉 `tools/pet_words.txt`、`books/pet.json`，并从 `index.html` 的 `BOOKS` 列表里去掉 `pet` 这一项即可。

## 字体

页面从 Google Fonts 在线加载 Baloo 2 与 站酷快乐体（ZCOOL KuaiLe），两者均为 SIL Open Font License 1.1。仓库里没有打包字体文件；字体加载不到时会自动改用系统字体。

---

## KyleBing/english-vocabulary — BSD 3-Clause License

```
BSD 3-Clause License

Copyright (c) 2022-2026, KyleBing

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

## skywind3000/ECDICT — MIT License

```
MIT License

Copyright (c) 2025 Linwei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
