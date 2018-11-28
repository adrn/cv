%-----------------------------------------------------------------------------
%	Class options
%

\ProvidesClass{apw-cv}[2018/11/21]
\NeedsTeXFormat{LaTeX2e}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass{article}

\usepackage[left=1in, right=1in, body={6.5in, 9.0in}]{geometry} % Page margins
\usepackage{hyperref} % Required for links
\usepackage{enumitem}


%-----------------------------------------------------------------------------
%	Colors
%

\usepackage[usenames, dvipsnames]{xcolor}

\definecolor{body}{HTML}{000000} % primary text color
\definecolor{sections}{HTML}{3086b4} % section heading color
\definecolor{subsections}{HTML}{666666} % subsection heading color
\definecolor{rules}{HTML}{cccccc} % for horizontal rules
\definecolor{links}{HTML}{3086b4} % link color
\definecolor{deemph}{HTML}{666666} % light grey

%-----------------------------------------------------------------------------
%	Font
%

\usepackage{fontspec}
\defaultfontfeatures{Mapping=tex-text}

\setmainfont[Color=body,
             Path=fonts/lato/,
             BoldItalicFont=Lato-RegIta,BoldFont=Lato-Reg,ItalicFont=Lato-LigIta]{Lato-Lig} % primary font, with bold and italic options

\setsansfont[Scale=MatchLowercase,
             Mapping=tex-text,
             Path=fonts/raleway/]{Raleway-ExtraLight} % sans-serif option?


%-----------------------------------------------------------------------------
%	Main document heading
%

\newcommand{\headersection}[2]{ % Defines the command for the main heading
    {
        \fontsize{20pt}{20pt} % Font size
        \fontspec[Path = fonts/lato/]{Lato-Reg}\selectfont #1 % name: use light font
        ~\color{rules}---~ \color{sections}
        \fontspec[Path = fonts/lato/]{Lato-Lig}\selectfont #2
        % \vspace{-0.5em}
    }
}

%-----------------------------------------------------------------------------
%	Section formatting
%

\setlength{\parindent}{0pt}
\setlength{\parskip}{\baselineskip}%

\usepackage{titlesec} % Required for customizing section/subsection/etc titles

\titlespacing{\section}{0pt}{0pt}{0pt} % Removes the spacing around the main section titles
\titlespacing{\subsection}{0pt}{0pt}{0pt} % Removes the spacing around the subsections

\titleformat{\section}{ % Customize the large section titles
\vspace{-0.2em}\color{sections}\scshape\fontspec[Path = fonts/lato/]{Lato-Bol}\fontsize{14pt}{16pt}\selectfont\raggedright}{}{0em}{}[{\vspace{-0.1em}\titlerule[0.2pt]\vspace{1em}}]

\titleformat{\subsection}{ % Customize the subsections and places worked/studied titles
\color{subsections}\fontspec[Path = fonts/lato/]{Lato-Reg}\fontsize{14pt}{16pt}}{}{0em}{}[{\vspace{0.4em}}]

% Make lists without bullets and compact spacing
\renewenvironment{itemize}{
  \begin{list}{}{
    \setlength{\leftmargin}{2em}
    \setlength{\itemsep}{0.em}
    \setlength{\parskip}{0pt}
    \setlength{\parsep}{0.25em}
    % \setlength{\itemindent}{0em}
  }
}{
  \end{list}
}

% %----------------------------------------------------------------------------------------
% %	SECTION TITLE STYLING AND SPACING
% %----------------------------------------------------------------------------------------
%
% \newenvironment{tightitemize} % Defines the tightitemize environment which modifies the itemize environment to be more compact
% {\vspace{-\topsep}\begin{itemize}[leftmargin=*]\normalsize\itemsep1pt \parskip0pt \parsep0pt}
% {\end{itemize}\vspace{-\topsep}}
