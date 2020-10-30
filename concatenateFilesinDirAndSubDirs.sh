logdir=$HOME/clef_docs
echo $logdir
for dir in "$logdir"/*/
do
  (
    for subdir in "$dir"*/
    do
      (
        cd "$subdir"
        echo $subdir
        file=($subdir.tsv )
        echo $file
      )
    done
  )
done
