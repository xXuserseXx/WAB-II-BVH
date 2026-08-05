%% provadis-thesis.cls
%% LaTeX class file for Provadis School of International Management and Technology
%% Scientific work template (WAB/Bachelor/Master thesis)
%% Based on template: Vorlage_WAB-BT-MT_Provadis-2023.pdf
%% created by Marlon Spangenberg, latex@zeile4.de
%% Co-author: Linus Jahn

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{provadis-thesis}[2025/10/23 v1.0 Provadis Thesis Class]

% Base class
\LoadClass[12pt,a4paper,oneside]{report}

% Required packages
%\RequirePackage[ngerman]{babel}
%\RequirePackage[nenglish]{babel}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{geometry}
\RequirePackage{graphicx}
\RequirePackage{setspace}
\RequirePackage{titlesec}
\RequirePackage{tocloft}
\RequirePackage{fancyhdr}
\RequirePackage{hyperref}
\RequirePackage[table]{xcolor}
\RequirePackage{ragged2e}  % For better text justification
\RequirePackage{etoolbox}  % For patching commands
\RequirePackage{calc}  % For length calculations
\RequirePackage{enumitem}
\RequirePackage{graphicx}
\RequirePackage[table,xcdraw0]{}
\RequirePackage{tabularx}
\RequirePackage{colortbl}
\RequirePackage{newtxtext,newtxmath}
\RequirePackage{array}
\RequirePackage{xltabular}

% Caption formatting package
\RequirePackage{caption}

% Redefine \large to be exactly 14pt (instead of default 14.4pt at 12pt base size)
\renewcommand{\large}{\fontsize{14}{17}\selectfont}

% Configure caption style with lines above and below
\DeclareCaptionFormat{provadis}{%
    \rule{\textwidth}{0.4pt}\par%
    \vspace{0pt}\noindent#1#2\textit{#3}\par%    % <-- Change the vspace value
    \vspace{-6pt}\rule{\textwidth}{0.4pt}%        % <-- Change the vspace value
}

\captionsetup{
    format=provadis,
    justification=raggedright,
    singlelinecheck=false,
    labelsep=space,
    font={normalsize},
    labelfont={normalsize}
}

% Custom abbreviation commands
\newlength{\maxabbrevwidth}
\setlength{\maxabbrevwidth}{0pt}

\newcommand{\measureabbrev}[1]{%
  \settowidth{\dimen0}{#1}%
  \ifdim\dimen0>\maxabbrevwidth
    \setlength{\maxabbrevwidth}{\dimen0}%
  \fi
}

\newcommand{\abbrev}[1]{%
  \measureabbrev{#1}%
  \rightskip=\maxabbrevwidth \dotfill\rlap{\hbox to \maxabbrevwidth{\hfill#1}}\par
}

\newcommand{\mycite}[2][]{%
  \if\relax\detokenize{#1}\relax
    (\cite{#2})%
  \else
    (p.#1, \cite{#2})%
  \fi
}

% Remove automatic page breaks before chapters
\patchcmd{\chapter}{\if@openright\cleardoublepage\else\clearpage\fi}{}{}{}
\patchcmd{\chapter}{\clearpage}{}{}{}

% Ensure special sections always start on new pages
% Save original commands
\let\oldtableofcontents\tableofcontents
\let\oldlistoffigures\listoffigures
\let\oldlistoftables\listoftables

% Redefine to include page breaks
\renewcommand{\tableofcontents}{%
    \clearpage
    \oldtableofcontents
}

\renewcommand{\listoffigures}{%
    \clearpage
    \oldlistoffigures
}

\renewcommand{\listoftables}{%
    \clearpage
    \oldlistoftables
}
\setlength{\cftfigindent}{0mm}
\setlength{\cfttabindent}{0mm}

% Ensure bibliography starts on new page
% Use AtBeginDocument to ensure biblatex is loaded before patching
\AtBeginDocument{%
    \@ifpackageloaded{biblatex}{%
        % Save the original command
        \let\oldprintbibliography\printbibliography
        % Redefine to include page break
        \renewcommand{\printbibliography}{%
            \cleardoublepage
            \oldprintbibliography
        }%
    }{}%
}

% Ensure unnumbered chapters (like Glossar, Abkürzungsverzeichnis) start on new pages
% by redefining \chapter* to always include clearpage
\let\oldchapterstar\@schapter
\def\@schapter#1{%
    \clearpage
    \oldchapterstar{#1}%
}


% Page geometry
\geometry{
    a4paper,
    left=3cm,    % 30mm left margin (binding side)
    right=2cm,     % 20mm right margin
    top=2.8cm,
    bottom=2cm,
    headheight=15pt,
    %headsep=12pt
}

% Line spacing
\setstretch{1.43}

% For title page elements, we use explicit \vspace commands with mm units

% Define custom commands for thesis information
\newcommand{\thesistitle}[1]{\gdef\@thesistitle{#1}}
\newcommand{\thesistype}[1]{\gdef\@thesistype{#1}} % WAB/Bachelorarbeit/Masterarbeit
\newcommand{\coursename}[1]{\gdef\@coursename{#1}}
\newcommand{\degree}[1]{\gdef\@degree{#1}} % B.Sc. or M.Sc.
\newcommand{\studiengang}[1]{\gdef\@studiengang{#1}}
\newcommand{\matrikelnr}[1]{\gdef\@matrikelnr{#1}}
\newcommand{\studiengruppe}[1]{\gdef\@studiengruppe{#1}}
\newcommand{\studentemail}[1]{\gdef\@studentemail{#1}}
\newcommand{\studentphone}[1]{\gdef\@studentphone{#1}}
\newcommand{\firstsupervisor}[1]{\gdef\@firstsupervisor{#1}}
\newcommand{\secondsupervisor}[1]{\gdef\@secondsupervisor{#1}}
\newcommand{\submissiondate}[1]{\gdef\@submissiondate{#1}}

% Overwrite commands
\renewcommand{\cfttoctitlefont}{\Large\bfseries}
\renewcommand{\cftlottitlefont}{\Large\bfseries}
\renewcommand{\cftloftitlefont}{\Large\bfseries}
\setlength{\cftbeforetoctitleskip}{0pt}  % Space before TOC title (default 50pt)
\setlength{\cftaftertoctitleskip}{10pt}  % Space after TOC title (default 40pt)
\setlength{\cftbeforelottitleskip}{0pt}  % Space before LOT title
\setlength{\cftafterlottitleskip}{10pt}  % Space after LOT title
\setlength{\cftbeforeloftitleskip}{0pt}  % Space before LOF title
\setlength{\cftafterloftitleskip}{10pt}  % Space after LOF title

% Default values
\gdef\@thesistitle{Titel der Arbeit}
\gdef\@thesistype{Bachelorarbeit}
\gdef\@coursename{}
\gdef\@degree{Bachelor of Science (B.Sc.)}
\gdef\@studiengang{XXX}
\gdef\@matrikelnr{XXX}
\gdef\@studiengruppe{XXX}
\gdef\@studentemail{email@example.com}
\gdef\@studentphone{}
\gdef\@firstsupervisor{XXX}
\gdef\@secondsupervisor{XXX}
\gdef\@submissiondate{TT.MM.JJJJ}

% Custom title page
\renewcommand{\maketitle}{
    \newgeometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}  % Title page uses 25mm margins
    \begin{titlepage}
        \thispagestyle{empty}  % No page number on title page
        % Precise positioning measurements
        % Logo: 20mm from left, 25mm from top
        % Document type: 65mm from top
        % Title: 15mm below document type
        % Coursename: 30mm below title
        
        % Position logo at 20mm from left edge of paper
        % Text area starts at 25mm (left margin), so move back 5mm
        \noindent
        \hspace*{-5mm}%
        \includegraphics[width=0.35\textwidth]{provadis-logo}
        
        % Document type should be at 65mm from top of page
        % Text area starts at 25mm, logo is roughly 20-25mm high
        % So we need: 65mm - 25mm - logo_height ≈ 20mm
        \vspace*{15mm}
        
        \centering
        
        % Document type at 65mm from page top
        {\normalsize \@thesistype \par}
        
        % Title: 15mm below document type
        \vspace{10mm}
        
        % Title section (now user-customizable)
        {\large\bfseries 
        \setstretch{1.5}  % Adjust this number (1.0 = single, 1.5 = 1.5x, 2.0 = double)
        \@thesistitle\par}
        
        % Coursename: 30mm below title
        \vspace{30mm}
        
        % Degree information with consistent 5mm line spacing
        {\normalsize
        \setstretch{1.5}  % Controls line spacing for entire block
        \ifx\@coursename\empty
            For the attainment of the academic degree
            
            '\@degree'
            
            in the study programm'\@studiengang'
        \else
            For the course: \@coursename \\
           
            in the study programm'\@studiengang'
        \fi
        \par}
        
        \vspace{15mm}
        
        % Institution
        {\normalsize
        \setstretch{1.5}
        Presented to the faculty of Computer Science at\\
        Provadis School of International Management and Technology\\
        by\par}
        
        \vspace{15mm}
        
        % Student information
        {\normalsize \@author\par}
        {\normalsize Student ID: \@matrikelnr\par}
        {\normalsize \@studiengruppe\par}
        {\normalsize \@studentemail\par}
        \ifx\@studentphone\empty
        \else
            {\normalsize \@studentphone\par}
        \fi
        
        \vfill
        
        % Supervisors and date
        \begin{flushleft}
        \begin{tabular}{@{}ll}
        First supervisor: & \@firstsupervisor \\[1mm]
        %Zweitgutachter: & \@secondsupervisor \\[1mm]
        Deadline: & \@submissiondate \\
        \end{tabular}
        \end{flushleft}
        
    \end{titlepage}
    \restoregeometry  % Restore normal margins (35mm left, 20mm right)
    \cleardoublepage
}

% Confidentiality notice (Sperrvermerk)
% Loads content from external sperrvermerk.tex file
\newcommand{\makeconfidentialitynotice}{
    \cleardoublepage
    \thispagestyle{empty}
    \chapter*{Sperrvermerk}
    \addcontentsline{toc}{chapter}{Sperrvermerk}
    
    \input{sperrvermerk}
    
    \cleardoublepage
}

\newcommand{\schapter}[1]{
	\chapter*{#1}
	\lhead{\textit{#1}}
	\addcontentsline{toc}{chapter}{#1}
}

% Declaration of authorship (English)
\newcommand{\makedeclaration}[3]{% #1 = place, #2 = date, #3 = path to signature
    \cleardoublepage
    \chapter{Declaration of Authorship}
    %\addcontentsline{toc}{chapter}{Declaration of Authorship}
    
    I hereby declare that I have written this thesis independently and without undue assistance, and that I have used no sources or aids other than those indicated. All passages that are quoted verbatim or paraphrased from other sources are clearly identified as such. The drawings, figures, and tables contained in this thesis were created by me or have been provided with an appropriate source reference. This thesis has not been submitted by me, in the same or a similar form, to any other institution of higher education for the purpose of obtaining an academic degree.
    
    \vspace{2cm}
    
    \noindent
    #1, #2
    
    \vspace{2cm}
    
    \noindent
	\includegraphics[height=2cm]{#3}\\[1ex]
    \rule{7cm}{0.4pt}\\
    \@author
    
    \cleardoublepage
}


% AI usage directory (KI-Verzeichnis)
\newcommand{\makeaidirectory}{
    \cleardoublepage
    \chapter{KI-Verzeichnis}
    
    %Jede Nutzung von KI ist zu dokumentieren. Dazu wird hinter dem Literaturverzeichnis ein separates KI-Verzeichnis eingefügt, das alle KI-generierten Inhalte, die eingesetzten Systeme, die verwendeten „Prompts" sowie die weitere Verwendung des Outputs der KI transparent macht.
    
    \vspace{0.5cm}
    
    %Bei der mehrfachen Verwendung eines Systems werden die Einträge durchnummeriert. Die Reihenfolge der Einträge entspricht der Reihenfolge der Verwendung im Text. Das KI-Verzeichnis ist verpflichtend.
    
    \vspace{1cm}
    
    % Table will be inserted here by user
    
    \cleardoublepage
}

% Chapter and section formatting
% All titles: 14pt
% Using 'hang' format instead of 'display' to prevent page breaks
% Removed \chaptertitlename to hide "Kapitel" word
\titleformat{\chapter}[hang]
    {\normalfont\fontsize{14}{17}\bfseries}{\thechapter}{1em}{\fontsize{14}{17}\bfseries}
% Made the before spacing conditional;
% It is found in the \pretocmd{chapter}{code}{success}{failure}
% Every \chapter is followed by a \parskip by default
% A parskip has the size of 6pt as measured by the Debug macro bellow.
% The debug macro writes its measurement of parskip to the .log file.
% 1 mm = 0,284 pt
% The Word document has an a chapter to text distance of 3mm.
% This equals 8.5 pt.
% Because the \parskip has 6pt we still have to add
% 2.5 pt via the \titlespacing.
% The world document has a distance of 11.5 mm between header and
% the \chapter title.
% This equals 32.7 pt.
% Because the \headsep has 25 pt and the topskip accounts for 12 pt
% We do already have a total of 32pt.
% Additionally, there are approximately 2mm (~5,6pt)
% 'inexplicable distance' between header and \chapter.
% Therefor, we have a total of 37.6 pt by default.
% We need to subtract 5.6 pt if the chapter is at the top.
% This was done in the if branch of the \pretocmd

% If a chapter is not at the very top of the page,
% The space above the chapter should equal 6mm.
% 6pt are already occupied by a parskip
% Therefor we need 11 pt of additional space.
% This was done in the else branch of the \pretocmd
\titlespacing*{\chapter}{0pt}{0pt}{2.5pt}

%  Debug macro:
% Just place the \debugspacing command anywhere in the .tex
% It will print the message "[DEBUG] parskip=6.0pt"
% Which proofs that parskips are 6.0pt.
% The call for to \debugparskip in .tex has been omitted before pushing.
% But you can always verify, by adding it in yourself.
\makeatletter
\newcommand{\debugparskip}{%
  \typeout{[DEBUG] parskip=\the\parskip}%
}
\makeatother
% Just place the \debugheadsep command anywhere in the .tex 
% It will print the message "[DEBUG] parskip=25.0pt"
% Which proofs that parskips are 6.0pt.
% The call for to \debugheadsep in .tex has been omitted before pushing.
% But you can always verify, by adding it in yourself.
\makeatletter
\newcommand{\debugheadsep}{%
  \typeout{[DEBUG] headsep=\the\headsep}%
}
\makeatother
% For debugging, we eliminiate all things that could cause vspace
% Between header and title.
% Found that \headsep and \topskip are responsible for
% 90% of distance between header and title.
% \setlength{\headsep}{0pt}
% \setlength{\topskip}{0pt}
% Performing analogous debugging procedure to get the pt val of
% topskip.
% Found out that \topskip = 12pt
\makeatletter
\newcommand{\debugtopskip}{%
  \typeout{[DEBUG] topskip=\the\topskip}%
}
\makeatother



\makeatletter
\pretocmd{\chapter}{%
	% pagetotal is an internal LaTex tracker of vertical space above
	% If we are on a new page, then pagetotal=0pt is true
	% In this case we don't want any custom before space caused by our \chapter
  \ifdim\pagetotal=0pt
  	\vspace*{-5.6pt}
    % Top of page → no added vertical space
  \else
	% Otherwise give it the default 18pt
    \vspace*{11pt}% Same spacing that used to be titlespacing-before
  \fi
}{}{}
\makeatother



% Section titles: 14pt bold
\titleformat{\section}
    {\normalfont\fontsize{14}{17}\bfseries}{\thesection}{1em}{}
\titlespacing*{\section}{0pt}{18pt}{9pt}  % 18pt before, 9pt after
    
% Subsection titles: 12pt bold
\titleformat{\subsection}
    {\normalfont\fontsize{12}{17}\bfseries}{\thesubsection}{1em}{}
\titlespacing*{\subsection}{0pt}{18pt}{9pt}  % 18pt before, 9pt after
    
% Subsubsection titles: 12pt italic
\titleformat{\subsubsection}
    {\normalfont\fontsize{12}{17}\itshape}{\thesubsubsection}{1em}{}
\titlespacing*{\subsubsection}{0pt}{18pt}{9pt}  % 18pt before, 9pt after

% Customize chapter marks for headers (remove "Kapitel" word)
\renewcommand{\chaptermark}[1]{%
    \markboth{#1}{}%
}

% Headers and footers
\pagestyle{fancy}
\fancyhf{}  % Clear all headers and footers
% Page number at top right
\fancyhead[R]{\textit{\thepage}}
% Chapter/section name at top left
\fancyhead[L]{\nouppercase{\leftmark}}
% Clear footer (no page number at bottom)
\fancyfoot{}
% Underline the entire header
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% Style for chapter start pages (redefine plain style)
\fancypagestyle{plain}{%
    \fancyhf{}  % Clear all
    \fancyhead[R]{\textit{\thepage}}  % Page number on right
	\fancyhead[L]{\nouppercase{\textit{\leftmark}}}
    \fancyfoot{}  % No footer
    \renewcommand{\headrulewidth}{0.4pt}
    \renewcommand{\footrulewidth}{0pt}
}

% Front matter and main matter commands
% Use \frontmatter after title page for Roman numerals (i, ii, iii, ...)
% Use \mainmatter when content starts for Arabic numerals (1, 2, 3, ...)

\newcommand{\frontmatter}{
    \cleardoublepage
    \pagenumbering{roman}  % Roman numerals: i, ii, iii, iv, ...
    \setcounter{page}{1}   % Start at i
    % Front matter header: only page number on right, left side empty
    \fancyhead[L]{\nouppercase{\textit{\leftmark}}}  % Restore chapter names in italics
}

\newcommand{\mainmatter}{
    \cleardoublepage
    \pagenumbering{arabic}  % Arabic numerals: 1, 2, 3, 4, ...
    \setcounter{page}{1}    % Restart at 1
    % Main matter header: chapter name on left, page number on right
    \fancyhead[L]{\nouppercase{\textit{\leftmark}}}  % Restore chapter names in italics
    % Update plain style to also show chapter names
	\makeatletter
    \fancypagestyle{plain}{%
        \fancyhf{}
        \fancyhead[R]{\textit{\thepage}}
		\fancyhead[L]{\nouppercase{\textit{\firstmark}}} 
        \fancyfoot{}
        \renewcommand{\headrulewidth}{0.4pt}
        \renewcommand{\footrulewidth}{0pt}
    }%
	\makeatother
    % Text formatting for main matter
    \setlength{\parindent}{0pt}  % No paragraph indentation
    \setlength{\parskip}{6pt}    % Small space between paragraphs instead
}

\newcommand{\backmatter}{
    \cleardoublepage
}

% Table of contents formatting
\setlength{\cftbeforechapskip}{10pt}

% Hyperref setup
\hypersetup{
    colorlinks=true,
    linkcolor=black,
    filecolor=black,
    urlcolor=blue,
    citecolor=black,
    pdfborder={0 0 0}
}

\endinput