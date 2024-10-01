import time
import torch  
import argparse
from options.train_options import TrainOptions
from data import create_dataset
from models import create_model
from util.visualizer import Visualizer
import os  # Ajouté pour utiliser os.path.join

# Fonction pour filtrer les éléments 'None' dans le batch
def custom_collate_fn(batch):
    # Filtrer les éléments 'None'
    batch = [b for b in batch if b is not None]
    
    # Si le batch est vide, retourner None pour qu'il soit ignoré dans la boucle d'entraînement
    if len(batch) == 0:
        return None
    
    # Sinon, retourner le batch normal
    return torch.utils.data.default_collate(batch)

if __name__ == '__main__':
    # Utiliser argparse pour gérer les arguments de la ligne de commande
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu_ids', type=str, default='-1', help='ID(s) of the GPU to use; -1 for CPU')
    parser.add_argument('--dataroot', type=str, default='deepcrack/datasets/DeepCrack/', help='path to the dataset')
    parser.add_argument('--name', type=str, default='deepcrack', help='name of the experiment')
    parser.add_argument('--model', type=str, default='deepcrack', help='model to use')
    parser.add_argument('--dataset_mode', type=str, default='deepcrack', help='dataset mode')
    parser.add_argument('--batch_size', type=int, default=1, help='input batch size')
    parser.add_argument('--num_classes', type=int, default=1, help='number of classes')
    parser.add_argument('--load_width', type=int, default=256, help='image load width')
    parser.add_argument('--load_height', type=int, default=256, help='image load height')
    parser.add_argument('--loss_mode', type=str, default='focal', help='loss function to use')
    parser.add_argument('--niter', type=int, default=400, help='number of epochs to train')
    parser.add_argument('--niter_decay', type=int, default=300, help='number of epochs to decay learning rate')
    parser.add_argument('--phase', type=str, default='train', help='train, val, test, etc')  # Ajoutez la phase ici
    parser.add_argument('--serial_batches', action='store_true', help='if true, the data is not shuffled')  # Ajouté ici
    parser.add_argument('--num_threads', type=int, default=1, help='number of threads for data loading')  # Ajouté ici
    parser.add_argument('--max_dataset_size', type=int, default=float('inf'), help='Maximum number of samples to load')  # Ajouté ici
    parser.add_argument('--isTrain', action='store_true', help='if true, the model is trained')  # Ajouté ici
    parser.add_argument('--checkpoints_dir', type=str, default='./checkpoints', help='directory to save checkpoints')  # Ajouté ici
    parser.add_argument('--preprocess', type=str, default='resize_and_crop', help='preprocessing method')  # Ajouté ici
    parser.add_argument('--display_sides', type=bool, default=False, help='Whether to display sides of the output images')  # Ajouté ici
    parser.add_argument('--input_nc', type=int, default=3, help='number of input channels for the model')  # Ajouté ici
    parser.add_argument('--ngf', type=int, default=64, help='number of filters in the generator')  # Ajouté ici
    parser.add_argument('--norm', type=str, default='instance', help='normalization type: instance | batch | none')  # Ajouté ici
    parser.add_argument('--init_type', type=str, default='normal', help='initialization type')  # Ajouté ici
    parser.add_argument('--init_gain', type=float, default=0.02, help='scaling factor for initialization')  # Ajouté ici
    parser.add_argument('--load_iter', type=int, default=0, help='the iteration number to load from')  # Ajouté ici
    parser.add_argument('--epoch', type=int, default=1, help='current epoch')  # Ajouté ici

    # Options for the visualizer
    parser.add_argument('--display_id', type=int, default=1, help='window id of the visualizer')  # Ajouté ici
    parser.add_argument('--display_winsize', type=int, default=256, help='window size for display')  # Ajouté ici
    parser.add_argument('--display_port', type=int, default=8097, help='port of the visualizer')  # Ajouté ici
    parser.add_argument('--display_ncols', type=int, default=4, help='number of columns for displaying images')  # Ajouté ici
    parser.add_argument('--display_server', type=str, default='http://localhost', help='Visdom server address')  # Ajouté ici
    parser.add_argument('--display_env', type=str, default='main', help='Visdom display environment')  # Ajouté ici

    # Récupérer les arguments
    opt = parser.parse_args()

    # Ajouter les options à TrainOptions
    train_options = TrainOptions()
    train_options.dataroot = opt.dataroot
    train_options.name = opt.name
    train_options.model = opt.model
    train_options.dataset_mode = opt.dataset_mode
    train_options.batch_size = opt.batch_size
    train_options.num_classes = opt.num_classes
    train_options.load_width = opt.load_width
    train_options.load_height = opt.load_height
    train_options.loss_mode = opt.loss_mode
    train_options.niter = opt.niter
    train_options.niter_decay = opt.niter_decay
    train_options.gpu_ids = opt.gpu_ids
    train_options.phase = opt.phase  # Ajoutez la phase ici
    train_options.serial_batches = opt.serial_batches  # Ajoutez la ligne pour gérer serial_batches
    train_options.num_threads = opt.num_threads  # Ajoutez la ligne pour gérer num_threads
    train_options.max_dataset_size = opt.max_dataset_size  # Ajoutez la ligne pour gérer max_dataset_size
    train_options.isTrain = opt.isTrain  # Ajoutez la ligne pour gérer isTrain
    train_options.checkpoints_dir = opt.checkpoints_dir  # Ajouté ici
    train_options.preprocess = opt.preprocess  # Ajouté ici
    train_options.display_sides = opt.display_sides  # Ajouté ici
    train_options.input_nc = opt.input_nc  # Ajouté ici
    train_options.ngf = opt.ngf  # Ajouté ici
    train_options.norm = opt.norm  # Ajouté ici
    train_options.init_type = opt.init_type  # Ajouté ici
    train_options.init_gain = opt.init_gain  # Ajouté ici
    train_options.load_iter = opt.load_iter  # Ajouté ici
    train_options.epoch = opt.epoch  # Ajouté ici
    train_options.display_id = opt.display_id  # Ajouté ici
    train_options.display_winsize = opt.display_winsize
    train_options.display_port = opt.display_port
    train_options.display_ncols = opt.display_ncols
    train_options.display_server = opt.display_server
    train_options.display_env = opt.display_env

    # Convertir les GPU IDs en liste d'entiers
    if train_options.gpu_ids == '-1':
        train_options.gpu_ids = []
    else:
        train_options.gpu_ids = [int(id) for id in train_options.gpu_ids.split(',')]

    dataset = create_dataset(train_options)  # create a dataset given opt.dataset_mode and other options

    # Utiliser custom_collate_fn dans le DataLoader pour gérer les 'None'
    dataset.dataloader.collate_fn = custom_collate_fn

    dataset_size = len(dataset)    # get the number of images in the dataset.
    print('The number of training images = %d' % dataset_size)

    model = create_model(train_options)      # create a model given opt.model and other options
    #model.setup(train_options)               # regular setup: load and print networks; create schedulers
    visualizer = Visualizer(train_options)   # create a visualizer that display/save images and plots
    total_iters = 0                # the total number of training iterations

    for epoch in range(train_options.epoch_count, train_options.niter + train_options.niter_decay + 1):    # outer loop for different epochs
        epoch_start_time = time.time()  # timer for entire epoch
        iter_data_time = time.time()    # timer for data loading per iteration
        epoch_iter = 0                  # the number of training iterations in current epoch, reset to 0 every epoch

        for i, data in enumerate(dataset):  # inner loop within one epoch
            # Vérifier si 'data' est None
            if data is None or len(data) == 0:
                print(f"Warning: Batch at index {i} is None or empty, skipping.")
                continue

            iter_start_time = time.time()  # timer for computation per iteration
            if total_iters % train_options.print_freq == 0:
                t_data = iter_start_time - iter_data_time
            visualizer.reset()
            total_iters += train_options.batch_size
            epoch_iter += train_options.batch_size
            model.set_input(data)         # unpack data from dataset and apply preprocessing
            model.optimize_parameters(epoch)   # calculate loss functions, get gradients, update network weights

            if total_iters % train_options.display_freq == 0:   # display images on visdom and save images to a HTML file
                save_result = total_iters % train_options.update_html_freq == 0
                model.compute_visuals()
                visualizer.display_current_results(model.get_current_visuals(), epoch, save_result)

            if total_iters % train_options.print_freq == 0:    # print training losses and save logging information to the disk
                losses = model.get_current_losses()
                t_comp = (time.time() - iter_start_time) / train_options.batch_size
                visualizer.print_current_losses(epoch, epoch_iter, losses, t_comp, t_data)
                if train_options.display_id > 0:  # if using visdom
                    visualizer.plot_current_losses(epoch, float(epoch_iter) / dataset_size, losses)

            if total_iters % train_options.save_latest_freq == 0:  # save the latest model
                print('saving the latest model (epoch %d, total_iterations %d)' % (epoch, total_iters))
                model.save_networks('latest')

            iter_data_time = time.time()  # timer for data loading per iteration

        # End of epoch
        if epoch % train_options.save_epoch_freq == 0:  # save the model to disk
            print('saving the model at the end of epoch %d' % epoch)
            model.save_networks('epoch_%d' % epoch if train_options.save_by_iter else 'latest')

        print('End of epoch %d / %d \t Time Taken: %d sec' % (epoch, train_options.niter + train_options.niter_decay, time.time() - epoch_start_time))
