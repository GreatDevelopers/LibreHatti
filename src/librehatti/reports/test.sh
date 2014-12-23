GLOBIGNORE="__init__.py"
i=0
while read line
do
    array[ $i ]="$line"        
    (( i++ ))
done < <(ls *.py)

for a in `seq 0 $i`
do
( echo -n ''; cat /home/jass/testing/licence.txt) >> ${array[$a]}
done
#printf -- '%s\n' "${array[@]}"
#echo ${array}
