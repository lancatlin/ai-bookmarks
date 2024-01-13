from transformers import pipeline

summarizer = pipeline(task="summarization")

# content = [
#     "In this paper, we tack lay summarization tasks, which aim to automatically produce lay summaries for scientific papers, to participate in the first CL-LaySumm 2020 in SDP workshop at EMNLP 2020. We present our approach of using Pre-training with Extracted Gap-sentences for Abstractive Summarization (PEGASUS; Zhang et al., 2019b) to produce the lay summary and combining those with the extractive summarization model using Bidirectional Encoder Representations from Transformers (BERT; Devlin et al., 2018) and readability metrics that measure the readability of the sentence to further improve the quality of the summary. Our model achieves a remarkable performance on ROUGE metrics, demonstrating the produced summary is more readable while it summarizes the main points of the document.",
#     "我們可以從四個命令中可以學到的幾個概念： 命令 ls 在執行時不用其他參數就可以顯示出當前目錄底下的內容。 根據這樣的概念延伸後來舉個例子，如果我們想秀出一個不在目錄的資料夾 pypy 的內容。我們可以在命令後加上一個位置參數。會用位置參數這樣的名稱是因為程式會知道輸入的參數該做的事情。這樣的概念很像另一個命令 cp，基本的使用方式是 cp SRC DEST。第一個位置參數代表的是想要複製的目標，第二個位置的參數代表的則是想要複製到的地方。 現在我們想再增加一些，要顯示除了檔名之外更多的資訊。在這裡就可以選擇加上 -l 這個參數。 這是 help 文件的片段。對於以前從未使用過的程序來說非常有用，可以透過這些 help 文件來了解這些該怎麼使用。",
# ]

with open("ResNet.html", "r") as f:
    content = f.read()
    summary = summarizer(content[:1024])
    print(summary)
