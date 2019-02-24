> 之前遇到过一个问题，在 Windows 系统使用 UTF-8 的文件，在 Linux 系统中会乱码。于是发现了带 BOM 的 UTF-8 格式。
#### 带BOM的 UTF-8 格式  
  
BOM：Byte Order Mark，就是字节序标记。  

维基百科中 BOM 的描述，如下：  

The byte order mark (BOM) is a Unicode character, U+FEFF BYTE ORDER MARK (BOM), whose appearance as a magic number at the start of a text stream can signal several things to a program reading the text:  
- The byte order, or endianness, of the text stream;
- The fact that the text stream's encoding is Unicode, to a high level of confidence;
- Which Unicode encoding the text stream is encoded as.  
  
从维基百科中我们可以知道，BOM 是在文本流开头的字节序标记，编码为 U+FEFF。  
  
但是我们的软件一般是识别 ASCII 码然后对文本流进行处理的，于是带 BOM 的 UTF-8 文件就导致软件无法识别，造成乱码现象。  
 
很多系统已经不使用带 BOM 的 UTF-8 文件了，只有 Windows 系统仍然保存着该格式，用以区分 UTF-8 和 ASCII 编码格式。所以在 Windows 系统下使用 UTF-8 需要特别注意。  