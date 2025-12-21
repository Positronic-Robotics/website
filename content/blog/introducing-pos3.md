Title: Introducing pos3: Python Context Manager for S3
Date: 2025-12-16
Category: Blog
Slug: introducing-pos3
Author: Positronic Team
Summary: We are releasing `pos3`, a lightweight Python library that makes working with S3 as simple as using local files.
Image: theme/positronic/static/img/pos3-banner.png

We released a small but powerful Python library called `pos3` to simplify working with S3.
We're not announcing this with as much fanfare as our main product, but we hope it will be useful to many of you.

**The Killer Feature:** It allows you to feed data from S3 into **any third-party code** (like Pandas, OpenCV, PyTorch) or legacy scripts that only understand local files. You don't need to rewrite all your I/O code to support `boto3` or `s3fs`!

### Why We Built It

We built `pos3` because we hit a wall while automating training and inference pipelines for our robotics models. We had dozens of scripts and standard tools that expected local files, and rewriting them all to use S3 APIs was a non-starter.

Now, `pos3` is a staple in our stack. You can find it used [throughout the Positronic codebase](https://github.com/Positronic-Robotics/positronic/search?q=pos3) to seamlessly bridge cloud storage with our runtime.

### The Problem

In ML workflows, we often have tools that expect local paths:
```python
cv2.imread('image.jpg')
pd.read_csv('data.csv')
torch.load('model.pt')
```

To use data from S3, you usually have to write boilerplate code to download the file to a temp directory, pass that path to the function, and maybe upload the result back. This clutters your logic with infrastructure concerns.

### The Solution

`pos3` solves this with a context manager. Inside the context, S3 buckets are mirrored to your local disk transparently.

```python
import pos3
import pandas as pd

# Inside the context, S3 feels like a local folder
with pos3.mirror():
    # pos3.download returns a standard pathlib.Path
    # It only downloads files if they changed (smart caching)
    path = pos3.download('s3://bucket/dataset')

    # Pandas doesn't even know the data came from S3
    df = pd.read_csv(path / 'data.csv')

    # Get a local folder that will sync back to S3
    results_dir = pos3.upload('s3://bucket/results')

    # Write to it as usual. Files are uploaded in the background
    # or when the context exits.
    df.to_csv(results_dir / 'processed.csv')
```

### Why not just use `s3fs`?

Libraries like `s3fs` mount S3 as a virtual filesystem. This is great for interactive exploration, but often **too slow** for heavy ML training loops or image processing pipelines because every read creates a network request.

`pos3` takes a different approach: **Local performance first**.
It syncs the data to your fast local SSD before your code runs. Your code then runs at full native disk speed. `pos3` handles the messy bits of checking file hashes, parallel downloading, and background uploading.

### Installation

It's available on PyPI:

```bash
pip install pos3
```

Check out the [README](https://github.com/Positronic-Robotics/pos3) for more advanced usage, like background syncing interval for long training jobs.
