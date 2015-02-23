cd $PWD"/templates/Test_Reports/"
sed -i -- 's/amp;/ /g' *.tex
pdflatex my_latex_tamplate_copy.tex
pdflatex trial_copy.tex
pdflatex -f trial_without_mix_copy.tex
pdflatex my_tamplate_without_mix_copy.tex
mv  *.pdf ../../../static/Download/
rm -f *.log
rm -f *.out
rm -f *.aux


