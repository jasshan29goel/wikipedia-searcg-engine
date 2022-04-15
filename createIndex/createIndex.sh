
time python3 indexer.py $1 seperateIndex singleTitle
echo "Seperate Indices Created\n\n"
time python3 mergeIndex.py seperateIndex singleIndex
rm -r seperateIndex
echo "Seperate Indices Merged\n\n"
time python3 mergeToken.py singleIndex singleTokenIndex
echo "Seperate Tokens Merged\n\n"
time python3 split.py singleTokenIndex $2
rm singleTokenIndex
echo "Index creation done\n\n"
time python3 split.py singleTitle $3
rm singleTitle
echo "Title split done"