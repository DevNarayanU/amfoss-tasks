# Git Commands


	    git add filename :: adds file to the staging area

	    git commit -o filename :: adds specific file only from the staging area with more than one files

	    .gitignore : *.filetype [ignores all files with filetypes]
				: folder/ [ignores the whole folder]
	
	 
		git merge branch:: merges the current branch upto the new commits of the
								new branch

		git stash :: saves your currrent work temp

		git stash pop :: reapplies the saved changes to working area

		git rebase branchname :: rewrites history

		git rm filename :: removes file from repo and working area
		git mv oldfilename newfilename :: renames to newfilename
		
		
		git commit --amend :: changes the last commit to new one
		git commit --amend --date=<date>:: just like it says, changes the date    
				of commiting
		git reflog :: shows commit history (kinda) 
		git rebase <committag> :: points the current branch to that commit 

		git resest HEAD~1 :: Undo the latest commit **and** unstage files, leaving them modified on disk so you can re-commit them separately.
	
		squash inside interactive mode to sort of merging multiple commits as of one commit

		git update-index :: can be used to add the execuatable bit ,, file should be executable in both local and git

		git add -p filname :: we can control what all things in the file to be staged through patching

		git cherry-pick branchname :: applies the latest change by some existing commits along different branches
		
		git rebase upstream branch --onto=newbase :: essentially makes commits in upstream and not in branch to newbase
		git log -S "word" :: searches the commits with that specific word
			git bisect run sh -c "openssl enc -base64 -A -d < home-screen-text.txt | grep -v jackass" :: given in the hint , I assume it works by running a shell with the given content again and again 
		

