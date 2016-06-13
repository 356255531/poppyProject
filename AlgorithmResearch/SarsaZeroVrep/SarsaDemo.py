# A simple SARSA Reinforcement Learning example as described for example in:
# "Reinforcement Learning Embedded in Brains and Robots"
# C. Weber, M. Elshaw, S. Wermter, J. Triesch and C. Willmot
# In: Reinforcement Learning: Theory and Applications (2008)
# http://www.books.i-techonline.com/book.php?id=23
# http://fias.uni-frankfurt.de/~cweber

# To run, first create a directory for the results:
#    mkdir /tmp/coco/
# Then run:
#    python SARSA.py
# The weights are written into "/tmp/coco/" as ".pnm" image files.
# To watch these image files conveniently, use lookpy.tcl as:
#    lookpy.tcl a w 0 1
# (Weights must exist first, so better use a 2nd xterm for this)
# (Parameters mean to see activation and weight files of areas 0 and 1)


import random
import numpy
import scipy
import pylab
import Image


# used by exporttiles()
# insert into file a comment which looks e.g. like this:  # highS: 0.099849  lowS: -0.099849
def exportinfo (filename, highS, lowS):
    f = open(filename, 'rb')
    content = f.read()
    f.close()
    f = open(filename, 'wb')
    charcount = 0
    for char in content:
        f.write(char)
        if charcount == 2:
           f.write('# highS: %.6f  lowS: %.6f\n' % (highS, lowS))
        charcount += 1
    f.close()


def exporttiles (X, x, y, a, b, frame, filename):
    xy, ab = numpy.shape(X)    
    if  (xy != x*y) or (ab != a*b):
        print 'imagetiles: size error'

    Y = numpy.zeros((frame + x*(a+frame), frame + y*(b+frame)))

    image_id = 0
    for xx in range(x):
        for yy in range(y):
            if image_id >= xy: 
                break
            tile = numpy.reshape (X[image_id], (a, b))
            beginA, beginB = frame + xx*(a+frame), frame + yy*(b+frame)
            Y[beginA : beginA+a, beginB : beginB+b] = tile
            image_id += 1

    im = Image.new ("L", (frame + y*(b+frame), frame + x*(a+frame)))
    im.info = 'comment here does not work'
    im.putdata (Y.reshape((frame + x*(a+frame)) * (frame + y*(b+frame))), offset=-Y.min()*255.0/(Y.max()-Y.min()), scale=255.0/(Y.max()-Y.min()) )
    im.save(filename, cmap=pylab.cm.jet)  # seems to ignore the colormap
    exportinfo (filename,  numpy.max(X), numpy.min(X))


class world_model_RL:
    def __init__(self, size_a, size_b):
        # init input position
        self.sel_a = random.randint (0, size_a-1)
        self.sel_b = random.randint (0, size_b-1)
        self.size_a = size_a
        self.size_b = size_b
        self.ind  = numpy.arange (0, self.size_a * self.size_b)
    def newinit(self):
        self.sel_a = random.randint (0, size_a-1)
        self.sel_b = random.randint (0, size_b-1)
    def act(self, act):
        # position world reaction
        if  numpy.random.random_sample() > 0.0:
            if  act == 0:
                self.sel_a -= 1
            elif act == 1:
                self.sel_b += 1
            elif act == 2:
                self.sel_a += 1
            elif act == 3:
                self.sel_b -= 1
            else:
                print 'action out of bounds'
        # position boundary conditions
        if   self.sel_a < 0:
            self.sel_a = 0
        elif self.sel_a >= self.size_a:
            self.sel_a = self.size_a - 1
        if   self.sel_b < 0:
            self.sel_b = 0
        elif self.sel_b >= self.size_b:
            self.sel_b = self.size_b - 1
    def reward(self):
        if  self.sel_a == 0 and self.sel_b == 2:
            return 1.0
        else:
            return 0.0
    def sensor(self):
        p = numpy.zeros(self.size_a * self.size_b)
        p[self.sel_a * self.size_a + self.sel_b] = 1.0
        return p


def rand_winner (S_from, beta):
    sum = 0.0
    p_i = 0.0
    rnd = numpy.random.random()
    d_r = len (S_from)
    sel = 0

    for i in range (d_r):
        sum += numpy.exp (beta * S_from[i])

    S_target = numpy.zeros (d_r)

    for i in range (d_r):
        p_i += numpy.exp (beta * S_from[i]) / sum

        if  p_i > rnd:
            sel = i
            rnd = 1.1 # out of reach, so the next will not be turned ON

    return sel


size_a, size_b = 16, 16
size_map = size_a * size_b
size_mot = 4
w_mot = numpy.random.uniform (0.0, 0.0, (size_mot, size_map))
world = world_model_RL(size_a, size_b)

beta = 50.0

for iter in range (10000):

    world.newinit()
    I = world.sensor()
    h = numpy.dot (w_mot, I)
    act = rand_winner (h, beta)                         # choose action
    act_vec = numpy.zeros (size_mot)
    act_vec[act] = 1.0
    val = numpy.dot (w_mot[act], I)                     # value before action
    r = 0
    duration = 0

    while r == 0:

        duration += 1

        world.act(act)                                  # do selected action
        r = world.reward()                              # read reward
        I_tic = world.sensor()                          # read new state

        h = numpy.dot (w_mot, I_tic)
        act_tic = rand_winner (h, beta)                 # choose next action

        act_vec = numpy.zeros (size_mot)
        act_vec[act] = 1.0

        val_tic = numpy.dot (w_mot[act_tic], I_tic)     # value after action

        if  r == 1.0:                                   # This is cleaner than defining
            target = r                                  # target as r + 0.9 * val_tic,
        else:                                           # because weights now converge.
            target = 0.9 * val_tic                      # gamma = 0.9
        delta = target - val                            # prediction error

        w_mot += 0.5 * delta * numpy.outer (act_vec, I)

        I[0:size_map] = I_tic[0:size_map]
        val = val_tic
        act = act_tic

    exporttiles (w_mot, 1, size_mot, size_a, size_b, 1, "/tmp/coco/obs_v_0_0.pgm")
    print iter, 'w_mot=%.2f..%.2f' % (numpy.min(w_mot), numpy.max(w_mot))

    print duration