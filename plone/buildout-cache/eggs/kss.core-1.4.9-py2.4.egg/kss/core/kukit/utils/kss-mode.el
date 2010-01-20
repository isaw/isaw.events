;;; kss.el --- KSS major mode

;; Copyright (C) 2001  Free Software Foundation, Inc.

;; Author: Jeroen Vloothuis
;; Keywords: extensions

;; This file is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 2, or (at your option)
;; any later version.

;; This file is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with GNU Emacs; see the file COPYING.  If not, write to
;; the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
;; Boston, MA 02111-1307, USA.

;;; Commentary:

;; This mode adds support for KSS (Kinetic Style Sheets).

;;

;;; Code:

(defvar kss-mode-map
  (let ((map (make-sparse-keymap)))
    (define-key map [foo] 'kss-do-foo)
    map)
  "Keymap for `kss-mode'.")

(defvar kss-mode-syntax-table
  (let ((st (make-syntax-table)))
    (modify-syntax-entry ?* ". 23")
    (modify-syntax-entry ?/ ". 14")
    st)
  "Syntax table for `kss-mode'.")

(defvar kss-font-lock-keywords
  `(
    ;; CSS selectors
    ("^\\([#_[:alnum:]][^:\n]+\\):[[:alnum:]-]+[[:blank:]]*{"
     (1 font-lock-constant-face)) 

    ;; Events
    (":\\([[:alnum:]-]+\\)[[:blank:]]*{"
     (1 font-lock-type-face))

    ;; Event parameters
    ("\\(evt-[[:alnum:]-]+\\):"
     (1 font-lock-type-face))

    ;; KSS keywords
    (,(concat (regexp-opt
               '("action-client" "action-server" 
                 "evt-load-initial" "evt-timeout-delay" 
                 "evt-timeout-repeat") t) ":")
     (1 font-lock-keyword-face))
    )
  "Keyword highlighting specification for `kss-mode'.")

;; (defvar kss-imenu-generic-expression
;;   ...)

;; (defvar kss-outline-regexp
;;   ...)

;;;###autoload
(define-derived-mode kss-mode fundamental-mode "KSS"
  "A major mode for editing KSS files."
  :syntax-table kss-mode-syntax-table

  (setq comment-start "/* "
        comment-end " */"
        comment-start-skip "/\\*[ \n\t]+")

  (set (make-local-variable 'comment-start) "/* ")
  (set (make-local-variable 'comment-end) " */")
  (set (make-local-variable 'comment-start-skip) "/\\*[ \n\t]+")
  
  (set (make-local-variable 'font-lock-defaults)
       '(kss-font-lock-keywords))
  (set (make-local-variable 'indent-line-function) 'kss-indent-line)
;;   (set (make-local-variable 'imenu-generic-expression)
;;        kss-imenu-generic-expression)
;;   (set (make-local-variable 'outline-regexp) kss-outline-regexp)
)

;;; Indentation

(defun kss-indent-line ()
  "Indent current line of KSS code."
  (interactive)
  (indent-line-to 
    (save-excursion
      (setq column (kss-calculate-indentation)))))
     

(defun kss-calculate-indentation ()
  "Return the column to which the current line should be indented."
  (forward-line -1)
  
  (cond ((re-search-forward "{[[:blank:]]*" 
                            (+ (line-end-position) 1) t) 4)
        ((looking-at "[[:blank:]]*}[[:blank:]]*$") 0)
        ((equal (point-min) (point)) 0)
        (t (kss-calculate-indentation))))


(provide 'kss-mode)
;;; kss.el ends here

