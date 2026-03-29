import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class DependencyMutationResultDto {
  @ApiProperty({ example: '67e6d0fd2f6b9d3f7d8d1234' })
  dependentId: string;

  @ApiPropertyOptional({ example: 2 })
  created?: number;

  @ApiPropertyOptional({ example: 1 })
  removed?: number;
}
