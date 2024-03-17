import os
import torch
from torch import nn


def load_lyrics(signer):
    text = ''
    os.chdir('data')
    subdirs = os.walk(signer)  # 读取每个子目录下的文本文件
    for root, _, files in subdirs:
        for file in files:
            f = open(root + os.sep + file, "r", encoding="utf-8")
            data = f.read().replace('\n', ' ').replace('\r', ' ')
            text += data
    text = text[0: min(10000, len(text))]
    char_list = list(set(text))                                                     # 索引 to 字符（列表）
    char2idx_dict = dict((char, idx) for idx, char in enumerate(char_list))         # 字符 to 索引（字典）
    idx_list = [char2idx_dict[char] for char in text]                               # 字符 to 索引（列表）
    input_size = len(char2idx_dict)                                                 # 输入数目
    return char_list, char2idx_dict, input_size, idx_list


def load_lyrics_iter(idx_list, device, batch_size=2, step_num=5):
    batch_num = len(idx_list) // batch_size                                         # batch 数目
    epoch_num = (batch_num - 1) // step_num                                         # 轮次
    idx_tensor = torch.tensor(idx_list, dtype=torch.float32, device=device)
    idx_tensor = idx_tensor[0: batch_size * batch_num].view(batch_size, batch_num)  # reshape
    for i in range(epoch_num):
        X = idx_tensor[:, i * step_num: (i + 1) * step_num]                         # 取相邻的小批量
        Y = idx_tensor[:, i * step_num + 1: (i + 1) * step_num + 1]
        yield X, Y


def to_one_hot(X, input_size):
    one_hot = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    for i in range(X.shape[1]):
        x = X[:, i].long()                                                               # 向下取整
        res = torch.zeros(x.shape[0], input_size, dtype=torch.float32, device=device)
        res.scatter_(1, x.view(-1, 1), 1)                                       # 转变为 one_hot
        one_hot.append(res)
    return torch.stack(one_hot)


class RNNModel(nn.Module):
    def __init__(self, input_size):
        super(RNNModel, self).__init__()
        self.rnn = nn.RNN(input_size=input_size, hidden_size=256)
        self.dense = nn.Linear(256, input_size)
        self.input_size = input_size
        self.state = None

    def forward(self, X, state):
        X = to_one_hot(X, self.input_size)
        Y, self.state = self.rnn(X, state)
        Y = self.dense(Y.view(-1, Y.shape[-1]))
        return Y, self.state


def train(model, lyrics_iter, criterion, optimizer):
    state = None
    train_loss = 0.0
    sample_num = 0
    for X, Y in lyrics_iter:
        if state is not None:
            state = state.detach()          # 使模型参数的梯度计算只依赖一次迭代读取的小批量序列，防止梯度计算开销太大
        optimizer.zero_grad()
        (output, state) = model(X, state)   # output: 形状为(num_steps * batch_size, vocab_size)

        y = torch.transpose(Y, 0, 1).contiguous().view(-1)      # Y 转置后再变成长度为 batch * num_steps 的向量
        loss = criterion(output, y.long())
        loss.backward()
        nn.utils.clip_grad_norm_(parameters=model.parameters(), max_norm=10, norm_type=2)
        optimizer.step()
        sample_num += y.shape[0]
        train_loss += loss.item() * y.shape[0]

    train_loss /= sample_num
    return train_loss


def generate(prefix, gen_len, model, char_list, char2idx_dict, device):
    state = None
    output = [char2idx_dict[prefix[0]]]
    for idx in range(gen_len + len(prefix) - 1):
        if state is not None:
            state = state.to(device)
        X = torch.tensor([output[-1]], device=device).view(1, 1)
        (Y, state) = model(X, state)
        if idx < len(prefix) - 1:
            output.append(char2idx_dict[prefix[idx + 1]])
        else:
            output.append(int(Y.argmax(dim=1).item()))
    return ''.join([char_list[idx] for idx in output])


def main():
    signer = input("请输入你想训练的歌手：")
    char_list, char2idx_dict, dict_size, idx_list = load_lyrics(signer)
    epoch_num, batch_size, lr = 250, 32, 1e-3
    gen_len = 140
    step_num = 10
    prefix = input("请输入前缀词：")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = RNNModel(dict_size)
    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epoch_num):
        lyrics_iter = load_lyrics_iter(idx_list, device, batch_size, step_num)
        perplexity = train(model, lyrics_iter, criterion, optimizer)
        if epoch % 50 == 0 and epoch:
            print('epoch %d, train_loss %f' % (epoch, perplexity))
            print('  ', generate(prefix, gen_len, model, char_list, char2idx_dict, device=device))


if __name__ == '__main__':
    main()
