// inspired by https://github.com/shu223/echo-library

vec3 normalizeColor(vec3 color)
{
    return color / max(dot(color, vec3(1.0/3.0)), 0.001);
}

kernel vec4 maskFromColor(sampler image, __color color, float threshold)
{
    float  d;
    vec4   p;

    // Compute distance between current pixel color and reference color
    p = sample(image, samplerCoord(image));
    d = distance(normalizeColor(p.rgb), normalizeColor(color.rgb));
    
    // If color difference is larger than threshold, return black.
    return  (d > threshold)  ?  vec4(0.0)  :  vec4(p.a);
}

kernel vec4 sampleAndScale(sampler image, float scale)
{
    return scale * sample(image, samplerCoord(image));
}

kernel vec4 coordinateMask(sampler mask, vec2 invSize)
{
    vec4  d;

    // Create a vector with (x,y, 1,1), normalizing the coordinates to 0-1 range
    d = vec4(destCoord()*invSize, vec2(1.0));

    // Return this vector weighted by the mask value
    return sample(mask, samplerCoord(mask))*d;
}

kernel vec4 centroid(sampler image)
{
    vec4  p;

    p = sample(image, samplerCoord(image));
    p.xy = p.xy / max(p.z, 0.001);
    return  p;
}
