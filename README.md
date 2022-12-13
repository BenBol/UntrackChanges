# UntrackChanges
Removes trackchanges from LaTeX

The LaTeX package [`trackchanges`](http://trackchanges.sourceforge.net/) is great! However, sometimes I want to quickly convert all the commands to plain LaTeX. This sometimes happens if I don't have `trackchanges` installed somewhere, or if it's interfering with the wordcount. This is where this python script comes in!

## Features

This script does three things:

1. Replaces `\added{...}` with the interior text.
2. Deletes `\removed{...}`.
3. Replaces `\changed{...}{...}` with the interior text of the second `{...}`.

**Warning:** This script will **not** check if the `trackchanges` commands are valid. I.e. if the curly brackets are unbalanced, this code will error.

## Usage

Currently, this is used as a script on a plain `.tex` file, e.g.

`python untrackchanges.py file.tex`

This will produce a new file with a `-untrack.txt` extension. 

## Todo

- [x] Complete tests
- [x] Add options for changes
- [x] Add checking before computations
- [x] Better file naming
