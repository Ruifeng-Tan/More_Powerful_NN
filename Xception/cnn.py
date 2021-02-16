"""
CNN modules.
"""
import torch.nn as nn
import torch

class DepthwiseSeparableConv(nn.Module):
    """
    Depth-wise separable convolution uses less parameters
    to generate output by convolution.
    :Examples:

    """

    def __init__(self, in_ch, out_ch, k, dim=1, bias=False):
        """
        :param in_ch: input hidden dimension size
        :param out_ch: output hidden dimension size
        :param k: kernel size
        :param dim: default 1. 1D conv or 2D conv
        :param bias: default False. Add bias or not
        """
        super().__init__()
        if dim == 1:
            self.depthwise_conv = nn.Conv1d(
                in_channels=in_ch, out_channels=in_ch,
                kernel_size=k, groups=in_ch, padding=k//2, bias=bias)
            self.pointwise_conv = nn.Conv1d(
                in_channels=in_ch, out_channels=out_ch,
                kernel_size=1, padding=0, bias=bias)
        elif dim == 2:
            self.depthwise_conv = nn.Conv2d(
                in_channels=in_ch, out_channels=in_ch,
                kernel_size=k, groups=in_ch, padding=k // 2, bias=bias)
            self.pointwise_conv = nn.Conv2d(
                in_channels=in_ch, out_channels=out_ch,
                kernel_size=1, padding=0, bias=bias)
        else:
            raise Exception("Incorrect dimension!")

    def forward(self, x):
        """
        :Input: (batch_num, in_ch, seq_length)
        :Output: (batch_num, out_ch, seq_length)
        """
        print(x)
        x = self.depthwise_conv(x)
        print(x)
        # depthwise的filter数量和通道的数量相同，每个通道只被一个filter卷积(通过groups控制)
        # 为了卷积之后的feature map的大小不变，使用padding补充损失的map尺寸
        # 由于depthwise的filter只能独立地针对一个channel卷积，忽略了cross-channel的信息
        # 于是需要使用pointwise_conv来学习cross-channel的信息，ponitwise就很类似于常规的卷积了,只不过他的kernel_size一定是 1*1
        # 其主要思想是解耦：使得参数的数量减少，在相同参数数量的情况下，就能搭建更深的网络，并且实验证明这种CNN结构可以更加有效地利用参数
        # 详情解说查看知乎：https://zhuanlan.zhihu.com/p/80041030
        return self.pointwise_conv(x)

if __name__ == '__main__':
    a = DepthwiseSeparableConv(10, 20, 5, dim=1)
    input = torch.randn(1, 10, 10)
    output = a(input)
    print(output.shape)