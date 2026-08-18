grep '^ATOM' $1 | grep ' CA ' | awk '
  {
    xsum += substr($0, 31, 8) + 0  # extract coordinate of X (column 31-38)
    ysum += substr($0, 39, 8) + 0  # extract coordinate of Y (clumn 39-46)
    zsum += substr($0, 47, 8) + 0  # extract coordinate of Z (column 47-54)
    cnt++
  }
  END {
    printf "Centroid: %.3f %.3f %.3f\n", xsum/cnt, ysum/cnt, zsum/cnt
  }'
