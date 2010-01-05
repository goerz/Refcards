%% 
%% This is file `arbitrary.cls'
%% 
%% Written by Hauke Voss 09.12.2002
%% Modified: 15.10.2004
%%
%% Based on: `a0poster.cls',
%% Copyright (C) 07.05.97 Gerlinde Kettl and Matthias Weiser

\ProvidesClass{arbitrary}[2002/12/04 v1.01 arbitrary class (Hauke Voss)]
\NeedsTeXFormat{LaTeX2e}[1995/06/01]
\LoadClass{article}

\newif\ifxnok
\newif\ifynok
\newif\ifmnok
\newif\ifymnok
\newif\ifdraft
\newif\iflandscape
\newif\ifposter

\newdimen\xcm
\newdimen\ycm
\newdimen\xmargin
\newdimen\ymargin
\newdimen\tbm
\newdimen\lrm
\newdimen\xoff
\newdimen\yoff
\newcount\xkoord
\newcount\ykoord
\newdimen\xp
\newdimen\yp

\xcm=21.0cm  % default: A4
\ycm=29.7cm
\xmargin=1in
\ymargin=1in

\xnoktrue
\ynoktrue
\mnoktrue
\ymnoktrue
\landscapefalse
\postertrue

\DeclareOption{a0+}{
\xcm=88.2cm  
\ycm=124.7cm
\xnokfalse
\ynokfalse
}

\DeclareOption{a0}{
\xcm=84.1cm  
\ycm=118.9cm
\xnokfalse
\ynokfalse
}

\DeclareOption{a1}{
\xcm=59.4cm  
\ycm=84.1cm
\xnokfalse
\ynokfalse
}

\DeclareOption{a2}{
\xcm=42.0cm  
\ycm=59.4cm
\xnokfalse
\ynokfalse
}

\DeclareOption{a3}{
\xcm=29.7cm  
\ycm=42.0cm
\xnokfalse
\ynokfalse
}

\DeclareOption{a4}{
\xcm=21.0cm  
\ycm=29.7cm
\xnokfalse
\ynokfalse
}

\DeclareOption{a5}{
\xcm=14.8cm  
\ycm=21.0cm
\xnokfalse
\ynokfalse
}

\DeclareOption{a6}{
\xcm=10.5cm  
\ycm=14.8cm
\xnokfalse
\ynokfalse
}

\DeclareOption{a7}{
\xcm=7.4cm  
\ycm=10.5cm
\xnokfalse
\ynokfalse
}

\DeclareOption{a8}{
\xcm=5.2cm  
\ycm=7.4cm
\xnokfalse
\ynokfalse
}

\DeclareOption{a9}{
\xcm=3.7cm  
\ycm=5.2cm
\xnokfalse
\ynokfalse
}

\DeclareOption{a10}{
\xcm=2.6cm  
\ycm=3.7cm
\xnokfalse
\ynokfalse
}

\DeclareOption{mpifr}{
\xcm=91.4cm  
\ycm=118.3cm
\xnokfalse
\ynokfalse
}

\DeclareOption{screen}{
\xcm=25cm  
\ycm=20cm
\xmargin=1.5cm
\ymargin=1.5cm
\xnokfalse
\ynokfalse
}

\DeclareOption{landscape}{
\landscapetrue
}
\DeclareOption{portrait}{
\landscapefalse
}
\DeclareOption{poster}{
\postertrue
}
\DeclareOption{small}{
\posterfalse
}
\DeclareOption*{
  \ifxnok
     \xcm=\CurrentOption
     \xnokfalse
  \else\ifynok
          \ycm=\CurrentOption
	  \ynokfalse
       \else\ifmnok
               \xmargin=\CurrentOption
	       \mnokfalse
            \else\ifymnok
                    \ymargin=\CurrentOption
	            \ymnokfalse
		 \else
		    \PackageWarning{arbitrary}{Unknown option \CurrentOption}
		 \fi
            \fi
       \fi
  \fi
}
\ExecuteOptions{21.0cm,29.7cm,5.5cm,portrait,final}
% = A4
\ProcessOptions\relax

\ifymnok
  \setlength{\ymargin}{\xmargin}
\fi

\iflandscape
   \newdimen\tausch
   \setlength{\tausch}{\xcm}
   \setlength{\xcm}{\ycm}
   \setlength{\ycm}{\tausch}
\fi

\setlength{\xoff}{\xmargin}
\setlength{\yoff}{\ymargin}

\multiply\xoff by -2
\multiply\yoff by -2

\setlength{\lrm}{\xmargin}
\setlength{\tbm}{\ymargin}

\advance\tbm by -1in
\advance\lrm by -1in

\xkoord=\xcm
\ykoord=\ycm
\divide\xkoord by 65536
\divide\ykoord by 65536
\xp=\xcm
\yp=\ycm
\advance\xp by \xoff
\advance\yp by \yoff

\setlength{\paperwidth}{\number\xkoord pt}
\setlength{\paperheight}{\number\ykoord pt}

\setlength{\textwidth}{\xp}
\setlength{\textheight}{\yp}

\setlength{\headheight}{0 cm}
\setlength{\headsep}{0 cm}
\setlength{\topmargin}{\tbm}
\setlength{\oddsidemargin}{\lrm}
\setlength{\evensidemargin}{\lrm}


\catcode`\%=11
\newwrite\Ausgabe
\immediate\openout\Ausgabe=arbitrary.ps
\write\Ausgabe{%%BeginFeature *PageSize arbitrary}
\write\Ausgabe{2 dict dup /PageSize [\number\xkoord\space \number\ykoord] put dup /ImagingBBox null put}
\write\Ausgabe{setpagedevice}
\write\Ausgabe{%%EndFeature}
\closeout\Ausgabe
\catcode`\%=14


\special{header=./arbitrary.ps}

\ifposter
   \input{arbitrary.sty}

   \renewcommand{\tiny}{\fontsize{12}{14}\selectfont}
   \renewcommand{\scriptsize}{\fontsize{14.4}{18}\selectfont}   
   \renewcommand{\footnotesize}{\fontsize{17.28}{22}\selectfont}
   \renewcommand{\small}{\fontsize{20.74}{25}\selectfont}
   \renewcommand{\normalsize}{\fontsize{24.88}{30}\selectfont}
   \renewcommand{\large}{\fontsize{29.86}{37}\selectfont}
   \renewcommand{\Large}{\fontsize{35.83}{45}\selectfont}
   \renewcommand{\LARGE}{\fontsize{43}{54}\selectfont}
   \renewcommand{\huge}{\fontsize{51.6}{64}\selectfont}
   \renewcommand{\Huge}{\fontsize{61.92}{77}\selectfont}
   \newcommand{\veryHuge}{\fontsize{74.3}{93}\selectfont}
   \newcommand{\VeryHuge}{\fontsize{89.16}{112}\selectfont}
   \newcommand{\VERYHuge}{\fontsize{107}{134}\selectfont}

   \setlength\smallskipamount{6pt plus 2pt minus 2pt}
   \setlength\medskipamount{12pt plus 4pt minus 4pt}
   \setlength\bigskipamount{24pt plus 8pt minus 8pt}

   \setlength\abovecaptionskip{25pt}
   \setlength\belowcaptionskip{0pt}
   \setlength\abovedisplayskip{25pt plus 6pt minus 15 pt}
   \setlength\abovedisplayshortskip{0pt plus 6pt}
   \setlength\belowdisplayshortskip{13pt plus 7pt minus 6pt}
   \setlength\belowdisplayskip\abovedisplayskip
\fi

\normalsize

\AtBeginDocument{
\special{papersize=\number\xkoord pt,\number\ykoord pt}
\pagestyle{empty}}

\endinput
%% 
%% End of file `arbitrary.cls'.
