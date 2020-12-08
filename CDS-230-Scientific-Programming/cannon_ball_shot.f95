program cannonBall
	! Program simulates the effects of gravity on a cannon ball shot. The user is prompted to input the total initial 
	! velocity of the cannon ball, and the angle of the shot. Program calculates the total time the ball was in the air
	! and the amount of distance that was traveled.
   	implicit none
	double precision:: g, y, x, h, vY, vX, totV, angle, pi, time
	
	print*, 'Enter a total velocity: '
	read(*,*) totV	
	print*, 'Enter sthe angle of the shot: '
	read(*,*) angle
	open(43, file='output.txt') 
	
	pi = acos(-1.0)
	g = 9.8
	vX = totV * cos((pi * angle)/180.d0)
	vY = totV * sin((pi * angle)/180.d0)
	y = 0.d0
	x = 0.d0
	h = .01d0
	time = 0.d0
	do 
		if(y.lt. 0.d0) exit 
		time = time + h
		y = y + h * vY
		vY = vY - h * g
		x = x + h * vX
		write(43, *) x, y
	enddo
	
	print*, 'Time: ', time , 'seconds.'
	print*, 'Total distance traveled: ', x
	close(43)
	print*, 'Done!'
end program cannonBall


