using Statistics 
p(x) = parse(Float64, x[6:end])

angle_diff(a, b) =
    if a < b
        a + (360 - b)
    else
        a - b
    end

angles = parse.(Float64, readlines(joinpath(@__DIR__, "angles_30_pct.txt")))
ds = []
for i in eachindex(angles)
    if i == lastindex(angles)
        break
    end
    d = angle_diff(angles[i], angles[i + 1])
    push!(ds, d)
end


