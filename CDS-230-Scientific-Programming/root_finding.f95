program rootFinding

   ! The purpose of this program is to find the roots of a function defined by the FORTRAN function myFunc and its 
   ! derivative derivMyFunc. The program asks the user for a starting 2 x points within the scope of the function myFunc.
   ! The signs of each input x value must have different signs. After gathering the x values, the program will then use the 
   ! x values to attempt calculate the roots using three different methods defined in seperate functions. 
	implicit none
	double precision:: x, tol, myFunc, derivMyFunc, bisect, newtonsMethod, secant, a, b, y, permA, permB
	tol = 1.0d-14 !set tolerance for 0
	
	do 
		print*, "Please enter two numbers seperated by a space : "
		read(*,*) permA, permB
		! check if the signs are opposite 
		if(sign(1.0d0, (permA * permB)) .lt. 0.0d0) then
			exit
		else
			print*, 'Error, the signs of input numbers must be opposite'
		endif
	enddo 
	
	! The following prints to the screen a root if it found it, the starting x values and number of iterations 
	! for each method.
	print*
	print*
	a = permA
	b = permB
	print*, 'Bisect Method'
	print*, 'A:', permA
	print*, 'B:', permB
	x = bisect(a, b, tol)
	print*, 'Root: ', x
	print*
	
	a = permA
	b = permB
	print*, 'Newtons Method'
	print*, 'Start:', permB
	x = newtonsMethod(b, tol)
	print*, 'Root: ', x
	print*
	
	a = permA
	b = permB
	print*, 'Secant Method'
	print*, 'A:', permA
	print*, 'B:', permB
	x = secant(a, b, tol)
	print*, 'Root: ', x
	print*
	print*, 'Done!'
	
end program rootFinding

function myFunc(x) result(y)
! Base function to find the root for 
	implicit none
	double precision:: x, y
	y = sin(x) + 1.5d0 - (.15d0 * x)
end function myFunc

function derivMyFunc(x) result(y)
! Derivative of myFunc
	implicit none
	double precision:: x, y
	y = cos(x)-(3.0d0/20.0d0)
end function derivMyFunc

function bisect(a, b, tolerance) result(m)
! Bisection method for root finding. Needs to be passed in two x values and a tolerance and will attempt to return the root 
! of the function myFunc. If no root is found, it will return 0 and print to the screen that you need to try different points.
! If the function loops more than 1000000 times the function will  exit as a precaution if it finds no root. 
	implicit none
	double precision:: a, b, m, tolerance, root, myFunc
	integer:: cnt

	do 
		m = (a + b)/2.0d0 
		if(abs(myFunc(m)) .lt. tolerance) then
			print*, 'Iterations from bisect method :', cnt
			exit 
		endif
		
		if(cnt .gt. 1000000) then 
			print*, 'No Root Found, Try Different Start Points'
			m = 0.0d0
			exit
		endif
		
		if(sign(1.0d0, myFunc(a)) .eq. sign(1.0d0, myFunc(m))) then 
			a = m
		else
			b = m
		endif
		
		cnt = cnt + 1
	enddo
end function bisect

function newtonsMethod(a, tolerance) result (m)
! Function that attempts to use Newtons method to find any roots to the function defined in myFunc.
! If the main loop goes to 50 the function will terminate and return 0 as the root. Needs to be passed in a starting 
! x point and a tolerance for finding the root of myFunc
	implicit none
	double precision:: a, m, tolerance, myFunc, derivMyFunc
	integer:: cnt
	cnt = 0
	do 
		m = a - (myFunc(a)/derivMyFunc(a))
		if(abs(myFunc(m)) .lt. tolerance) then 
			print*, "Iterations from Newton's method :", cnt
			exit
		else if(cnt .gt. 50) then 
			print*, 'Did not converge, please try a new starting point.'
			m = 0.0d0
			exit
		endif
		a = m 
		cnt = cnt + 1
	enddo
end function newtonsMethod

function secant(old, new, tolerance) result(m)
! Function trying to find the root of a function. Needs to be passed in two x values, an old one and a new one
! along with a tolerance. If the main loop goes to 1000000 the program will exit and return 0 as a root. 
	implicit none
	double precision:: old, new, m, temp, myFunc, tolerance
	integer:: cnt
	cnt = 0
	m = new
	do
		if(abs(myFunc(m)) .lt. tolerance) then
			print*, 'Iterations from secant method :', cnt
			exit
		else if(cnt .gt. 1000000) then
			print*, 'Too many iterations, try again.'
			m = 0.0d0
			exit
		end if 
		temp = m 
		m = m - myFunc(m)*((m - old)/(myFunc(m) - myFunc(old)))
		old = temp 
		cnt = cnt + 1
	enddo
end function secant