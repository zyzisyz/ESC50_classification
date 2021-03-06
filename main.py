#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
import os

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR

from models import ESC50_Dataset
from models import resnet34, resnet18

def train(args, model, device, train_loader, optimizer, epoch):
	model.train()
	for batch_idx, (data, target) in enumerate(train_loader):
		data, target = data.to(device), target.to(device)
		optimizer.zero_grad()
		output = model(data)
		loss = F.nll_loss(output, target)
		loss.backward()
		optimizer.step()
		if batch_idx % args.log_interval == 0:
			print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
				epoch, batch_idx * len(data), len(train_loader.dataset),
				100. * batch_idx / len(train_loader), loss.item()))
			if args.dry_run:
				break


def test(model, device, test_loader):
	model.eval()
	test_loss = 0
	correct = 0
	with torch.no_grad():
		for data, target in test_loader:
			data, target = data.to(device), target.to(device)
			output = model(data)
			test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
			pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
			correct += pred.eq(target.view_as(pred)).sum().item()

	test_loss /= len(test_loader.dataset)

	print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.4f}%)\n'.format(
		test_loss, correct, len(test_loader.dataset),
		100. * correct / len(test_loader.dataset)))


def main():
		# Training settings
	parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
	parser.add_argument('--batch-size', type=int, default=64, metavar='N',
			help='input batch size for training (default: 64)')
	parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
			help='input batch size for testing (default: 1000)')
	parser.add_argument('--epochs', type=int, default=14, metavar='N',
			help='number of epochs to train (default: 14)')
	parser.add_argument('--lr', type=float, default=1.0, metavar='LR',
			help='learning rate (default: 1.0)')
	parser.add_argument('--gamma', type=float, default=0.7, metavar='M',
			help='Learning rate step gamma (default: 0.7)')
	parser.add_argument('--no-cuda', action='store_true', default=False,
			help='disables CUDA training')
	parser.add_argument('--dry-run', action='store_true', default=False,
			help='quickly check a single pass')
	parser.add_argument('--seed', type=int, default=1, metavar='S',
			help='random seed (default: 1)')
	parser.add_argument('--log-interval', type=int, default=10, metavar='N',
			help='how many batches to wait before logging training status')
	parser.add_argument('--num-workers', type=int, default=10, help='how many workers to load the data')
	parser.add_argument('--ckpt-path', type=str, default="", help='ckpt')
	parser.add_argument('--ckpt-save-dir', type=str, default="ckpt", help='ckpt')
	parser.add_argument('--save-model', action='store_true', default=False,
			help='For Saving the current Model')
	args = parser.parse_args()

	use_cuda = not args.no_cuda and torch.cuda.is_available()
	torch.manual_seed(args.seed)

	device = torch.device("cuda" if use_cuda else "cpu")
	print("device: {}".format(device))

	train_kwargs = {'batch_size': args.batch_size}
	test_kwargs = {'batch_size': args.test_batch_size}
	if use_cuda:
		cuda_kwargs = {'num_workers': args.num_workers,
				'pin_memory': True,
				'shuffle': True}
		train_kwargs.update(cuda_kwargs)
		test_kwargs.update(cuda_kwargs)

	train_dataset = ESC50_Dataset(audio_dir="data/train", extension="fbank")
	test_dataset = ESC50_Dataset(audio_dir="data/test", extension="fbank")

	train_loader = torch.utils.data.DataLoader(train_dataset,**train_kwargs)
	test_loader = torch.utils.data.DataLoader(test_dataset, **test_kwargs)

	model = resnet18(num_classes=50).to(device)
	optimizer = optim.Adadelta(model.parameters(), lr=args.lr)

	## TODO ##
	epoch_start = 1
	if args.ckpt_path is not "":
		print("loaded {}".format(args.ckpt_path))
		model.load_state_dict(torch.load(args.ckpt_path))
		epoch_start = int(args.ckpt_path.split("_")[-1].split(".")[0]) + 1
	else:
		ckpts = os.listdir(args.ckpt_save_dir)
		if len(ckpts) is not 0:
			ckpts = [int(name.split("_")[-1].split(".")[0]) for name in ckpts]
			ckpts.sort()
			epoch_start = ckpts[-1]+1
			print("loaded {}/ckpt_{}.pt".format(args.ckpt_save_dir, ckpts[-1]))
			model.load_state_dict(torch.load("{}/ckpt_{}.pt".format(args.ckpt_save_dir, ckpts[-1])))

	scheduler = StepLR(optimizer, step_size=1, gamma=args.gamma)
	for epoch in range(epoch_start, args.epochs + 1):
		train(args, model, device, train_loader, optimizer, epoch)
		test(model, device, test_loader)
		scheduler.step()

		if args.save_model:
			torch.save(model.state_dict(), "{}/ckpt_{}.pt".format(args.ckpt_save_dir,epoch))


if __name__ == '__main__':
	main()


