\LoadClass{article}
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cube}[2011/03/26 My custom CV class]
\RequirePackage[ddmmyyyy]{datetime}
\RequirePackage{fancyhdr}
\RequirePackage{amssymb}
\RequirePackage{mathtools}
\RequirePackage{geometry}
\RequirePackage{hyperref}
\pagestyle{fancy}
\newcommand{\pagesettings}{
\geometry{
 a4paper,
 total={210mm,297mm},
 left=30mm,
 right=30mm,
 top=20mm,
 bottom=20mm,
 }
}
\newcommand{\topleft}[2]{
\begin{flushleft}
{#1}{\hfill{Dated:  #2}}
\end{flushleft}
}

\newcommand{\Reportheader}[1]{
\pagestyle{fancy}\lhead{#1}
}
\newcommand{\addressSection}[3]{
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
\newcommand{\signature}{
\begin{flushleft}
\bf{(Co-ordinator)}\hfill{Dean Testing \& Consultancy}
\end{flushleft}
}
