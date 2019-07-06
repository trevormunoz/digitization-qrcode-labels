#!/usr/bin/env python
# coding: utf-8

# # Creating labels for digitization workflow
# 
# 28 June 2019

# In[1]:


import segno
import labels
from uuid import uuid4
from PIL import Image
from reportlab.graphics import shapes


# ### Generate identifier data

# In[2]:


# Decide how many identifiers to generate. Printing to Avery 6874 labels so multiples of 6 make it easy
raw_ids = [uuid4() for x in range(1,31)]
idstr = [f"urn:uuid:{i}" for i in raw_ids]
human_str = [l[-6:] for l in idstr]
l_contents = list(zip(idstr, human_str))


# ### Generate QR codes
# 
# Importing QR codes into label maker as images seems to be easiest so we make a temporary directory to save images to as we generate them.

# In[3]:


import os, shutil, tempfile


# In[4]:


wd = tempfile.mkdtemp()


# In[5]:


wd


# In[6]:


# Encode the urn as a QR code; use the last six characters as a human-readable label to name the file

for tpl in l_contents:
    machine,human = tpl
    qr = segno.make_qr(machine)
    qr.save(os.path.join(wd, f"{human}.png"), scale=3, background=None)


# ### Set up label page

# In[7]:


specs = labels.Specification(215.9, 279.4, 2, 3, 95.25, 76.2)


# In[8]:


def write_content(label, width, height, filepath):
    
    # Create a shape for the QR code image and position it
    im = Image.open(filepath)
    imwidth, imheight = im.size
    a = shapes.Image(((width/2.0) - (imwidth/2.0)), 45, imwidth, imheight, filepath)
    
    # Create a human-readable label and position it
    human_readable = os.path.splitext(os.path.split(filepath)[1])[0]
    b = shapes.String(width/2.0, 15, human_readable, textAnchor="middle")
    
    # Create a space to write in a donor name
    c = shapes.String(30, (height-30), "Donor name: ")
    
    label.add(a)
    label.add(b)
    label.add(c)


# In[9]:


sheet = labels.Sheet(specs, write_content, border=True)


# In[10]:


files = [os.path.join(wd, f) for f in os.listdir(wd)]


# In[11]:


sheet.add_labels(files)


# Save the output to the current directory. To save somewhere else, supply a path.

# In[12]:


sheet.save('labels.pdf')


# Clean up our temporary working directory …

# In[13]:


shutil.rmtree(wd)

