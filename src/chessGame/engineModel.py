import torch
import torch.nn as nn
import torch.nn.functional as F

class ChessNet(nn.Module):
    def __init__(self):
        super(ChessNet, self).__init__()

        self.conv1 = nn.Conv2d(13, 64, kernel_size=3, padding=1) # 13 channels for the 12 piece types and an extra channel for the color the bot is playing
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        
        self.bn1 = nn.BatchNorm2d(64)
        self.bn2 = nn.BatchNorm2d(128)
        self.bn3 = nn.BatchNorm2d(128)

        self.res_conv1 = nn.Conv2d(13, 64, kernel_size=1)  # To match channels for residual
        self.res_conv2 = nn.Conv2d(64, 128, kernel_size=1)  # To match channels for residual
        
        #Positional encoding for the transformer
        self.positional_encoding = PositionalEncoding(d_model=128)

        #Transformer Encoder
        encoder_layers = nn.TransformerEncoderLayer(d_model=128, nhead=16)
        self.transformer = nn.TransformerEncoder(encoder_layers, num_layers=3)

        self.layer_norm = nn.LayerNorm(128)

        #Fully connected layer
        self.fc1 = nn.Linear(8*8*128, 4096)  #4096 possible moves

    def forward(self, x):

        residual = self.res_conv1(x)
        x = self.conv1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = x + residual
       # x += F.interpolate(residual, size=x.shape[2:]) 

        residual = self.res_conv2(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = F.relu(x)
        x = x + residual

        residual = x
        x = self.conv3(x)
        x = self.bn3(x)
        x = F.relu(x)
        x = x + residual

        x = x.view(-1, 128, 8*8)  #[batch_size, d_model, sequence_length]
        x = x.permute(2, 0, 1)  #[sequence_length, batch_size, d_model]

        # Positional encoding
        x = self.positional_encoding(x)

        # Transformer encoder
        x = self.transformer(x)

        x = self.layer_norm(x)

        x = x.permute(1, 0, 2).contiguous()  #[batch_size, sequence_length, d_model]
        x = x.view(-1, 8*8*128)
        x = self.fc1(x)
        return x

#Positional encoding for the transformer in order to give the model information about the position of the pieces
#Uses the sine and cosine functions to encode the position of the board in a unique way
#Experimental, might be overkill. Saw somewhere it could be useful for the transformer, but not sure if it is properly implemented here
class PositionalEncoding(nn.Module): 
    def __init__(self, d_model, max_len=64):
        super(PositionalEncoding, self).__init__()
        self.encoding = torch.zeros(max_len, d_model)
        self.encoding.requires_grad = False

        pos = torch.arange(0, max_len).float().unsqueeze(1)
        _2i = torch.arange(0, d_model, 2).float()

        self.encoding[:, 0::2] = torch.sin(pos / (10000 ** (_2i / d_model)))
        self.encoding[:, 1::2] = torch.cos(pos / (10000 ** (_2i / d_model)))
        self.encoding = self.encoding.unsqueeze(1)

    def forward(self, x):
        return x + self.encoding[:x.size(0), :].to(x.device)