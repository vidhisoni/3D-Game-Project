#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 textureCoordinate;
layout (location = 3) in ivec4 boneIndices;
layout (location = 4) in vec4 boneWeights;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform mat4 affineAnimationMatrix;
uniform mat4 boneTransformations[100];

uniform bool isAnimated;

out vec3 normals;
out vec4 worldPos;
out vec2 texCoord;
out vec3 cubeTexCoord;

void main()
{
	vec4 bonedPos = vec4(position, 1.0f);

	mat4 boneMatrix = mat4(1.0);
	if (isAnimated) {
		boneMatrix = boneTransformations[boneIndices[0]] * boneWeights[0];
		boneMatrix += boneTransformations[boneIndices[1]] * boneWeights[1];
		boneMatrix += boneTransformations[boneIndices[2]] * boneWeights[2];
		boneMatrix += boneTransformations[boneIndices[3]] * boneWeights[3];
	
		bonedPos = boneMatrix * bonedPos;
	}

    worldPos = modelMatrix * affineAnimationMatrix * bonedPos;
	normals = mat3(transpose(inverse(modelMatrix)) * affineAnimationMatrix * boneMatrix) * normal; // May be errored
	
	texCoord = textureCoordinate;

	gl_Position = projectionMatrix * viewMatrix * worldPos;
	cubeTexCoord = position;
}