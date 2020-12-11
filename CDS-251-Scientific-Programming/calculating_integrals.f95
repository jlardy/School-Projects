program integral

	! The purpose of this program is to use three different methods to find the area underneath the function defined in
	! the FORTRAN function myFunc. To use this program, you must enter in the start of the integral (a), the end of the integral (b),
	! and the size of the boxes that you would like to use. The program will then subdivide the total area (b-a) by the box size and 
	! calculate the area of boxes underneath the myFunc. After this is done, the program calls three different methods, midpoint,
	! trapezoid, and simpson. After each method completes running it will compare the calculated area to the real area for the intergral
	! [a:b] of myFunc and compute the absolute error and relative error. The program will print to the screen the area from the actual integral,
	! the method used' name, the computed area, and the absolute and relative errors.	
	!
   	implicit none
	double precision:: x, h, myFunc, y, midpoint, a, b, simpson, integralMyFunc, area, trapezoid, realArea, absoluteErr
	integer:: i, n
	
	
	print*, "Please enter two numbers seperated by a space : "
	read(*,*) a, b, h
	
	! compute the number of boxes that will fit between a and b
	n = int((b-a)/h)
	! find the area with the integral function 
	realArea = integralMyFunc(b) - integralMyFunc(a)
	print*, 'Area from actual integral', realArea
	print*
	
	! midpoint method
	area = midpoint(a, b, h, n)
	print*, 'Midpoint', area
	absoluteErr = realArea-area
	print*, 'Absolute Error', absoluteErr
	print*, 'Relative Error', (absoluteErr/realArea)*100
	print*
	
	! trapezoid method
	area = trapezoid(a, b, h, n)
	print*, 'Trapezoid', area
	absoluteErr = realArea-area
	print*, 'Absolute Error', absoluteErr
	print*, 'Relative Error', (absoluteErr/realArea)*100	
	print*

	! simpson's method
	area = simpson(a, b, h, n)
	print*, 'Simpson', area
	absoluteErr = realArea-area
	print*, 'Absolute Error', absoluteErr
	print*, 'Relative Error', (absoluteErr/realArea)*100 
	print*
	print*, 'Done!'
	
end program integral

function myFunc(x) result(y)
	! function definition, used as the function to find area under
	implicit none
	double precision:: x, y
	y = exp(-x) * (sin(x)**2)
end function myFunc

function midpoint(a, b, h, n) result(area)
	! Midpoint function to calculate the area underneath the function defined in myFunc
	! Returns the area of n rectangles of width h
	implicit none
	double precision:: a, b, h, x, area, myFunc
	integer:: i, n
	area = 0.0d0
	do i=1,n
		x = a + float(i-1) * h + (.5 * h)
		area = area + (myFunc(x) * h)
	enddo	
end function midpoint

function trapezoid(a, b, h, n) result(area)
	! Trapezoid function to calculate the area underneath the function defined in myFunc
	! Returns the area of n trapezoids of width h
	implicit none
	double precision:: a, b, h, x1, x2, myFunc, area
	integer:: i, n
	area = 0.0d0
	do i=1, n
		x1 = a + float(i-1) * h
		x2 = a + float(i) * h
		area = area + ((h/2)*(myFunc(x1) + myFunc(x2)))
	enddo
end function trapezoid

function simpson(a, b, h, n) result(area)
	! Simpson function to calculate the area underneath the function defined in myFunc
	! Applies same methods for finding the x values of boxes as both the midpoint and trapezoid
	! methods. Area calculation is done by combining parts of midpoint and trapezoid methods.
	implicit none
	double precision:: a, b, h, x1, x2, x3, myFunc, area
	integer:: i, n
	area = 0.0d0
	do i=1,n
		x1 = a + float(i-1) * h
		x2 = a + float(i-1) * h + (.5 * h)
		x3 = a + float(i) * h
		area = area + ((h/6.0d0)*(myFunc(x1) + (4.0d0 * myFunc(x2)) + myFunc(x3)))  
	enddo	
end function simpson

function integralMyFunc(x) result(y)
	! simplified integral function used find the real area underneath the equation myFunc. To use 
	! subtract integralMyFunc(b) - integralMyFunc(a)
	implicit none
	double precision:: x, y
	y = (exp(-x)/10.0d0)*(cos(2.0d0*x) - (2 * sin(2.0d0 * x)) - 5.0d0)
end function integralMyFunc