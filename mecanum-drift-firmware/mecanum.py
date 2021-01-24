# https://en.wikipedia.org/wiki/Mecanum_wheel

_VEC_X   = ( 1, -1, -1,  1)
_VEC_Y   = (-1, -1,  1,  1)
_VEC_PHI = (-1, -1, -1, -1)

class MecanumDrive:
    """provide motor control values for a mecanum wheel vehicle"""

    def move(self, cx=0, cy=0, cphi=0):
        """translate movement in the given direction to motor speeds for the four quadrants

        Input is the vector with two translational and one rotational values.
        The vector length must not exceed the value 1. Output is a vector of
        four motor control values. The maximum forward rotation is represented
        by 1, standstill by 0 and maximum reverse rotation by -1.
        """
        if abs(cx) + abs(cy) + abs(cphi) > 1:
            raise Exception('L-1 norm of movement vector ({}, {}, {}) may not be greater than 1'.format(cx, cy, cphi))

        return (cx * _VEC_X[0] + cy * _VEC_Y[0] + cphi * _VEC_PHI[0],
                cx * _VEC_X[1] + cy * _VEC_Y[1] + cphi * _VEC_PHI[1],
                cx * _VEC_X[2] + cy * _VEC_Y[2] + cphi * _VEC_PHI[2],
                cx * _VEC_X[3] + cy * _VEC_Y[3] + cphi * _VEC_PHI[3],)


if __name__ == '__main__':
    md = MecanumDrive()

    assert(md.move() == (0, 0, 0, 0))

    assert(md.move(cx=1) == (1, -1, -1, 1))
    assert(md.move(cx=-1) == (-1, 1, 1, -1))

    assert(md.move(cy=1) == (-1, -1, 1, 1))
    assert(md.move(cy=-1) == (1, 1, -1, -1))

    assert(md.move(cphi=1) == (-1, -1, -1, -1))
    assert(md.move(cphi=-1) == (1, 1, 1, 1))

    assert(md.move(cx=0.5, cy=0.5) == (0, -1, 0, 1))
    assert(md.move(cx=0.5, cy=-0.5) == (1, 0, -1, 0))

    assert(md.move(cx=+0.25, cy=+0.25, cphi=+0.25) == (-0.25, -0.75, -0.25,  0.25))
    assert(md.move(cx=-0.25, cy=+0.25, cphi=+0.25) == (-0.75, -0.25,  0.25, -0.25))
    assert(md.move(cx=+0.25, cy=-0.25, cphi=+0.25) == ( 0.25, -0.25, -0.75, -0.25))
    assert(md.move(cx=-0.25, cy=-0.25, cphi=+0.25) == (-0.25,  0.25, -0.25, -0.75))
    assert(md.move(cx=+0.25, cy=+0.25, cphi=-0.25) == ( 0.25, -0.25,  0.25,  0.75))
    assert(md.move(cx=-0.25, cy=+0.25, cphi=-0.25) == (-0.25,  0.25,  0.75,  0.25))
    assert(md.move(cx=+0.25, cy=-0.25, cphi=-0.25) == ( 0.75,  0.25, -0.25,  0.25))
    assert(md.move(cx=-0.25, cy=-0.25, cphi=-0.25) == ( 0.25,  0.75,  0.25, -0.25))
