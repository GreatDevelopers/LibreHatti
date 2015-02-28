\LoadClass{article}
\NeedsTeXFormat{LaTeX2e}
\RequirePackage[ddmmyyyy]{datetime}
\RequirePackage{geometry}
\ProvidesClass{trials}
\RequirePackage{amssymb}
\RequirePackage{mathtools}
\RequirePackage{fullpage}
\RequirePackage{graphicx}
\RequirePackage{fancyhdr}


 %%\fancyhead{}
 %%\lipsum

\newcommand{\pagesettings}{
\geometry{
 a4paper,
 total={210mm,297mm},
 left=30mm,
 right=10mm,
 top=10mm,
 bottom=20mm,
 }
 }

 
\newcommand{\logo}[1]{

\includegraphics[scale=0.3]{#1}
}

\newcommand{\sentext}[8]{
\Large\scshape\bf{#1}\\
\large\bf{#2}\\
\small\bf{#3}\\
\small{#4}\\
\small{#5}\\
\small\bf{#6}\\
\small\bf{#7}\hfill
\small\bf{#8}\\

}


\newcommand{\topleft}[2]{\vspace{0.5cm}
\begin{flushleft}
{#1}\hfill{#2}\raggedright
\end{flushleft}
}


\newcommand{\addressSection}[3]{
\vspace{0.5cm}
\begin{flushleft}
To\\
\hskip 1cm {#1}\\
\hskip 1cm {#2}\\
\hskip 1cm {#3}\\
\end{flushleft}
}
\newcommand{\subject}[2]{
\begin{flushleft}
\small\bf{#1}
\begin{minipage}[t]{5in} 
\textnormal{#2}
\end{minipage} 
\end{flushleft}

}

\newcommand{\refrence}[5]{
\begin{flushleft}
\small\bf{#1}{\textnormal{#2}{#3 }\textnormal{#4}\textnormal{#5}}
\end{flushleft}
}

\newcommand{\footer}[3]{

\begin{flushleft}
\begin{enumerate}
\item{#1}
\item{#2}
\item{#3}
\end{enumerate}
\end{flushleft}
}
\newcommand{\signature}[2]{
\vspace{0.5cm}
\begin{flushleft}
\bf{#1}\hfill{#2}
\end{flushleft}
}
