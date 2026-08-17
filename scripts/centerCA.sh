grep '^ATOM' $1 | grep ' CA ' | awk '
  {
    xsum += substr($0, 31, 8) + 0  # 提取 X 坐标（第31-38列）
    ysum += substr($0, 39, 8) + 0  # 提取 Y 坐标（第39-46列）
    zsum += substr($0, 47, 8) + 0  # 提取 Z 坐标（第47-54列）
    cnt++
  }
  END {
    printf "Centroid: %.3f %.3f %.3f\n", xsum/cnt, ysum/cnt, zsum/cnt
  }'
